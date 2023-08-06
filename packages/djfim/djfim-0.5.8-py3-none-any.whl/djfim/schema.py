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
# djfim.schema

from dmprj.engineering.schema.bief import BIEFField, BIEFEntity

from .function import Codec


class NormalizedPath(object):
    '''
    provide normalized path/URI
    '''

    FMT_APP_LABEL = 'app={app_label}'
    FMT_MOD_NAME  = 'model={model_name}'
    FMT_ANCHOR    = 'pk={anchor}'

    def __init__(self, obj):
        assert obj is not None, 'invalid value'
        super().__init__()
        self._obj = obj

    @property
    def data(self):
        return getattr(self, '_obj', dict())

    def __str__(self):
        SEP = ','
        uri = [
            self.FMT_ANCHOR.format(**self.data),
            self.FMT_MOD_NAME.format(**self.data),
            self.FMT_APP_LABEL.format(**self.data),
        ]
        try:
            base = self.get_base()
            assert base is not None, 'skip'
            base = base.strip()
            assert len(base) > 0, 'empty'
            uri.append(base)
        except:
            pass
        return SEP.join(uri)


class ExtendedBIEF(object):

    LABEL_DN      = 'dn'

    FLAG_ENCODED  = ':'
    FLAG_RELATION = '::'


class ExtendedBIEFField(BIEFField, ExtendedBIEF):
    '''
    extended BIEF field
    '''

    TYPE_PLAIN    = 0
    TYPE_ENCODED  = 1
    TYPE_RELATION = 2

    def get_value_type_flag(self):
        flag = ''
        try:
            if self.data['_type'] == self.TYPE_ENCODED:
                flag = self.FLAG_ENCODED
            elif self.data['_type'] == self.TYPE_RELATION:
                flag = self.FLAG_RELATION
        except KeyError:
            pass
        return flag

    @property
    def name(self):
        return self.data['name']

    @property
    def value(self):
        rval = self.data['value']
        try:
            if self.data['_type'] == self.TYPE_ENCODED:
                rval = Codec().to_representation(self.data['value'])
        except KeyError:
            pass
        return rval


class BIEFModel(BIEFEntity):
    '''
    extension to base class
    '''

    FMT_DN        = 'DN: {dn}'
    FMT_PLAINTEXT = '{k}: {v}'
    FMT_ENCODED   = '{k}:: {v}'
    FMT_RELATION  = '{k}::: {v}'

    def __init__(self):
        super().__init__()
        self._fields = list()

    def get_dn(self):
        dn = None
        try:
            dn = [ f for f in self._fields if f.name == f.LABEL_DN ][0]
        except:
            raise ValueError('missing DN field')
        return dn

    def get_fields(self):
        af = [ f for f in self._fields if f.name != f.LABEL_DN ]
        return af

    def get_field_name(self, f):
        return f.name

    def get_sorted_fields(self):
        return sorted(self.get_fields(), key=self.get_field_name)

    def append(self, f):
        self._fields.append(f)
        return None


class BIEFDumper(object):
    '''
    convert data to BIEF
    '''

    def get_entity(self):
        self.entity = BIEFModel()
        return self

    def append(self, data):
        f = ExtendedBIEFField()
        f.data = data
        self.entity.append(f)
        return None

    def __str__(self):
        return str(self.entity)


class BIEFLoader(object):
    '''
    convert BIEF to data
    '''
