# -*- python -*-
#
# Copyright 2021, 2022, 2023 Cecelia Chen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# djfim.contrib.schema

from django.contrib.auth import get_user_model
from django.db import models

from ..function import Codec
from ..runtime import DynamicBlock
from ..schema import BIEFDumper, BIEFLoader, ExtendedBIEF, ExtendedBIEFField, NormalizedPath


class EntityURI(NormalizedPath):

    DF = (
        'anchor',
        'model_name',
        'app_label',
    )

    @property
    def data(self):
        d = dict()
        for f in self.DF:
            d[ f ] = getattr(self._obj, f, None)
        return d


class URIParser(DynamicBlock):

    CLASS_URI = 'djfim.contrib.schema.EntityURI'

    def __init__(self):
        super().__init__()
        self.load_preset()

    def load_preset(self):
        self.uri_kls = self.getDynClass(self.CLASS_URI)
        self.uri_field_hub = dict()
        for item in ('FMT_ANCHOR','FMT_MOD_NAME','FMT_APP_LABEL'):
            fmt = getattr(self.uri_kls, item).split('=', 1)
            self.uri_field_hub[ fmt[0] ] = fmt[1].strip('{}')
        return self

    def parseURI(self, uri):
        d = dict()

        _lt = [ y.strip() for y in uri.split(',') ]
        path = [ x for x in _lt if len(x) > 0 ]
        for element in path:
            tokens = element.split('=', 1)
            if tokens[0] in self.uri_field_hub:
                internal_key = self.uri_field_hub[ tokens[0] ]
                d[ internal_key ] = tokens[1]

        assert len(d) == len(self.uri_field_hub), 'invalid input'
        return d


class fromDict(BIEFDumper, DynamicBlock):
    '''
    convert from dict to BIEF
    '''

    CLASS_PATH = 'djfim.contrib.schema.EntityURI'

    def __init__(self, dm, data):
        super().__init__()
        self._dm = dm
        self._data = data

    @property
    def user_dm(self):
        if not hasattr(self, '_USER_DM'):
            setattr(
                self,
                '_USER_DM',
                get_user_model()
            )
        return self._USER_DM

    @property
    def path_cls(self):
        return self.getDynClass(self.CLASS_PATH)

    def get_all_fk(self):
        fk = [ f for f in self._dm._meta.fields if f.related_model is not None ]
        return fk

    def get_sorted_af(self):
        af = [ f for f in self._dm._meta.fields if f.related_model is None ]
        af = [ x for x in af if x.name != 'id' ]
        return sorted(af)

    def get_sorted_fk(self):
        fk = self.get_all_fk()
        fk = [ x for x in fk if x.related_model._meta.label != self.user_dm._meta.label ]
        return sorted(fk)

    def generate_dn(self):
        pk = self._workcopy.pop('id')
        dn = {
            'name': 'dn',
            'value': self.path_cls(
                {
                    'anchor': pk,
                    'model_name': self._dm._meta.model_name,
                    'app_label': self._dm._meta.app_label,
                }
            ),
            '_type': ExtendedBIEFField.TYPE_PLAIN,
        }
        self.append(dn)
        return self

    def get_attr_type_code(self, f):
        rval = ExtendedBIEFField.TYPE_ENCODED
        if isinstance(f, (models.IntegerField, models.CharField)):
            rval = ExtendedBIEFField.TYPE_PLAIN
        return rval

    def generate_attr(self):
        af = self.get_sorted_af()
        for f in af:
            k = f.name
            v = self._workcopy[k]
            pt = {
                'name': k,
                'value': v,
                '_type': self.get_attr_type_code(f),
            }
            self.append(pt)
            pass
        return self

    def generate_relation(self):
        fk = self.get_sorted_fk()
        for k in fk:
            try:
                v = self._workcopy.pop(k.name)  # name may not in dict;
                rl = {
                    'name': k.name,
                    'value': self.path_cls(
                        {
                            'anchor': v,
                            'model_name': k.related_model._meta.model_name,
                            'app_label': k.related_model._meta.app_label,
                        }
                    ),
                    '_type': ExtendedBIEFField.TYPE_RELATION,
                }
                self.append(rl)
            except KeyError:
                pass
            pass
        return self

    def doConvert(self):
        self.get_entity()

        # make a copy to work, avoid changing the original;
        self._workcopy = dict()
        self._workcopy.update(self._data)

        self.generate_dn().generate_relation().generate_attr()
        # clean-up;
        delattr(self, '_workcopy')
        return self


class toDict(ExtendedBIEF):
    '''
    convert from BIEF to dict
    '''

    WHITESPACE = ' '
    KVSEP      = ': '

    def __init__(self, lines):
        super().__init__()
        self._lines = lines
        self.preload()
        pass

    def preload(self):
        cache = list()
        for line in self._lines:
            slime = line.rstrip()
            assert len(slime) > 0, 'empty line within a block'
            cache.append(slime)
            pass

        count = len(cache)
        assert count > 0, 'empty block'
        fc = [ l.startswith(self.WHITESPACE) for l in cache ]
        assert fc[0] == False, 'broken block'
        group = [ i for i in range(count) if fc[i] == False ]
        group.append(count)
        assert len(group) >= 2, 'broken block'

        fields = list()
        for g in range(len(group) - 1):
            slice = cache[ group[g] : group[g+1] ]
            fields.append(
                ''.join(
                    [ l.strip() for l in slice ]
                )
            )
            pass
        self._dn = fields[0]
        self._attr = fields[1:]

        self._dict = dict()
        for aline in self._attr:
            try:
                af = self.parse_relation(aline)
            except AssertionError:
                af = self.parse_attr(aline)
            self._dict[ af[0] ] = af[1]
            pass
        return self

    @property
    def dn(self):
        return self.parse_dn(self._dn)[1]

    def get_attribute(self, name):
        '''
        :param name: (string)
        '''
        if name == self.LABEL_DN:
            return self.dn
        return self._dict[name]

    @property
    def dict(self):
        '''
        :return: (dict)
        '''
        d = dict()
        d.update(self._dict)
        d[ self.LABEL_DN ] = self.dn
        return d

    def parse_dn(self, line):
        k, val = line.split(self.KVSEP, 1)
        assert k.lower() == self.LABEL_DN, 'invalid block'
        return (self.LABEL_DN, val)

    def parse_attr(self, line):
        kf, val = line.split(self.KVSEP, 1)
        if kf.endswith(self.FLAG_ENCODED):
            # value is encoded
            try:
                val = Codec().to_python(val)
            except:
                # caller/accessor of the encoded field should check validity of the value;
                pass
            pass
        k = kf.rstrip(':')
        assert len(k) > 0, 'empty attribute name'
        new_attr = (k, val)
        return new_attr

    def parse_relation(self, line):
        kf, val = line.split(self.KVSEP, 1)
        assert kf.endswith(self.FLAG_RELATION), 'invalid attribute flag'
        k = kf.rstrip(':')
        assert len(k) > 0 and len(k)+2 == len(kf), 'invalid attribute name or flag'
        new_attr = (k, val)
        return new_attr


class BIEFFileReader(BIEFLoader, DynamicBlock):
    CLASS_BLOCK = 'djfim.contrib.schema.toDict'

    def __init__(self):
        super().__init__()
        self.load_preset()

    def load_preset(self):
        self.block_kls = self.getDynClass(self.CLASS_BLOCK)

        self._cache = list()
        return self

    def __iter__(self):
        for item in self._cache:
            yield item

    def readFromFile(self, f):
        stream = f.read()
        chunk = stream.split('\n\n')
        for each in chunk:
            try:
                item = self.block_kls(each.splitlines())
                self._cache.append(item)
            except:
                pass
        return self
