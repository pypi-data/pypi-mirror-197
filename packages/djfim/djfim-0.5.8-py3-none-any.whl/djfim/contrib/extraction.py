# -*- python -*-
#
# Copyright 2021, 2022, 2023 Cecelia Chen
# Copyright 2018, 2019, 2020, 2021 Liang Chen
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
# djfim.contrib.extraction

from ..runtime import DynamicBlock


class AbstractArchiver(DynamicBlock):

    def __init__(self, context):
        super().__init__()
        self.load_preset()
        self._context = context

    def load_preset(self):
        self._pool = None
        return self

    def setHead(self, head):
        assert head is not None, 'invalid input'
        self._head = head
        return self

    def doArchive(self, obj):
        data = self.convertObjectToDict(obj)
        node = self._head.pool.addEntity(data)
        self.calculateDigest(node)
        return self

    def convertObjectToDict(self, obj):
        d = dict()
        # need subclass to define this;
        return d

    def calculateDigest(self, node):
        solver_kls = self._context.getDigestSolver()
        solver = solver_kls(node)
        return solver.updateNode()


class Archiver(AbstractArchiver):
    CLASS_CONTENT_CONVERT = 'djfim.contrib.schema.fromDict'

    def convertObjectToDict(self, obj):
        d = {
            'content': '',
        }
        convertor = self.getDynClass(self.CLASS_CONTENT_CONVERT)
        try:
            xd = dict()
            xd.update(obj.__dict__)
            excluded = [ k for k in xd.keys() if k.startswith('_') ]
            for k in excluded:
                xd.pop(k, None)

            fd = convertor(
                dm=obj.__class__,
                data=xd
            )
            d['content'] = fd.doConvert()
        except:
            pass
        return d


class BaseExtractor(DynamicBlock):
    CLASS_DATAMODEL_SOLVER  = 'djfim.solver.DMSolver'

    def __init__(self, context):
        super().__init__()
        self.load_preset()
        self._context = context

    def load_preset(self):
        self.dm_solver_kls = self.getDynClass(self.CLASS_DATAMODEL_SOLVER)
        return self

    @property
    def SOURCE_DM(self):
        return self.dm_solver_kls().get_model_class(self.data_model_name)

    def do(self, cache, head=None):
        self._sink = cache
        self._target = head

        self.preExtract()
        self.doExtractData()
        self.postExtract()
        return self

    def preExtract(self):
        return self

    def doExtractData(self):
        raise NotImplementedError('virtual method')

    def postExtract(self):
        return self


class Extractor(BaseExtractor):

    def doExtractData(self):
        self.qset = self.SOURCE_DM.objects.all()
        return self

    def postExtract(self):
        self._sink.append(self.qset)
        return self
