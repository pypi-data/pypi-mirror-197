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
# djfim.contrib.notary

import hashlib

from ..runtime import DynamicBlock


class DigestSolver(DynamicBlock):

    def __init__(self, node):
        super().__init__()
        self.load_preset()
        self._node = node

    def load_preset(self):
        self.output = ''
        self.storage_digest_attr = 'digest'
        return self

    def updateNode(self):
        self.do()
        setattr(self._node._obj, self.storage_digest_attr, self.output)
        self._node.doSave()
        return self

    def calculate(self, data):
        rval = hashlib.sha256(data.encode()).hexdigest()
        return rval

    def do(self):
        self.output = self.calculate(self._node.content)
        return self

    @property
    def node(self):
        return self._node


class ImprintSolver(DynamicBlock):

    def __init__(self, node):
        super().__init__()
        self.load_preset()
        self._node = node

    def load_preset(self):
        self.output = None
        self.storage_imprint_attr = 'imprint'
        return self

    def updateNode(self):
        self.do()
        setattr(self._node._obj, self.storage_imprint_attr, self.output)
        self._node.doSave()
        return self

    def generateImprimt(self, data):
        rval = None
        try:
            kls = self.getDynClass('djfim.extension.SaltedImprint')
            rval = kls(data).do()
        except:
            pass
        return rval

    def do(self):
        self.output = self.generateImprimt(self._node.digest)
        return self

    @property
    def node(self):
        return self._node
