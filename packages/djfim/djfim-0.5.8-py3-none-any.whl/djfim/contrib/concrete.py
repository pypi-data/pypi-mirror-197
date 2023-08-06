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
# djfim.contrib.concrete

from ..base import ENTITY as _ENTITY, GENERATION as _GENERATION
from ..runtime import DynamicBlock


class Entity(_ENTITY):
    CLASS_URI = 'djfim.contrib.schema.EntityURI'

    def __init__(self, obj):
        assert obj is not None, 'invalid value'
        super().__init__()
        self.load_preset()
        self._obj = obj

    def load_preset(self):
        self._uri_kls = DynamicBlock().getDynClass(self.CLASS_URI)
        return self

    @property
    def uri(self):
        return str(self._uri_kls(self._obj))

    @property
    def dn(self):
        FMT = 'dn: {v}'
        return FMT.format(v=self.uri)

    @property
    def anchor(self):
        return self._obj.anchor

    @property
    def obj_kls(self):
        rval = '{a}.{m}'.format(
            a=self._obj.app_label,
            m=self._obj.model_name,
        )
        return rval

    @property
    def content(self):
        return self._obj.content

    @property
    def digest(self):
        return self._obj.digest

    def toBIEF(self):
        text = list()
        text.append(self.dn)
        text.append(self.content)
        return '\n'.join(text)

    def copyAsDict(self):
        aCopy = dict()
        aCopy['uri'] = self.uri
        aCopy['content'] = self.content
        aCopy['digest'] = self.digest
        return aCopy


class Generation(_GENERATION):
    LABEL_LINK_A = 'a_link'
    LABEL_LINK_B = 'b_link'

    CLASS_URI = 'djfim.schema.NormalizedPath'

    def __init__(self, obj, parent=None, pool=None):
        assert obj is not None, 'invalid value'
        super().__init__()
        self.load_preset()
        self._obj = obj
        #
        self._parent = parent
        self._pool = pool

    def load_preset(self):
        self._uri_kls = DynamicBlock().getDynClass(self.CLASS_URI)
        return self

    @property
    def timestamp(self):
        return self._obj.time_stamp

    @property
    def memo(self):
        return self._obj.memo

    @property
    def digest(self):
        return self._obj.digest

    @property
    def imprint(self):
        return self._obj.imprint

    @property
    def uri(self):
        d = {
            'anchor': self.storage_pk,
            'model_name': '_head_',
            'app_label': 'djfim',
        }
        return str(self._uri_kls(d))

    def copyAsDict(self):
        aCopy = dict()
        aCopy['uri'] = self.uri
        aCopy['timestamp'] = self.timestamp
        aCopy['memo'] = self.memo
        aCopy['digest'] = self.digest
        aCopy['imprint'] = self.imprint
        return aCopy

    def toBIEF(self):
        text = list()
        text.append('dn: '+self.uri)
        text.append('timestamp: '+self.timestamp.isoformat())
        if self.memo is not None:
            text.append('memo: '+self.memo)
        if self.digest is not None:
            text.append('digest: '+self.digest)
        if self.imprint is not None:
            text.append('imprint: '+self.imprint)
        return '\n'.join(text)

    @property
    def content(self):
        lines = [
            self.timestamp.isoformat(),
            '' if self.memo is None else self.memo,
        ]
        return '\n'.join(lines)

    @property
    def storage_pk(self):
        return self._obj.id

    def getEntitySet(self):
        for blob in self.getCollection():
            yield self._pool.getEntity(blob)

    def getCollection(self):
        return self._pool.getCollection(self)

    def lookUpEntity(self, uri:str):
        # a) decode uri;
        # b) query the record;
        return NotImplementedError('todo')

    @property
    def parent(self):
        return self._parent

    @property
    def pool(self):
        return self._pool

    def setLink(self, side, dest, by_pk=False):
        assert side in (self.LABEL_LINK_A, self.LABEL_LINK_B), 'invalid input'

        if side == self.LABEL_LINK_A:
            attr = 'a_link'
        if side == self.LABEL_LINK_B:
            attr = 'b_link'
        if by_pk:
            attr = attr + '_id'

        setattr(self._obj, attr, dest)
        return self

    def doSave(self):
        self._obj.save()
        return self
