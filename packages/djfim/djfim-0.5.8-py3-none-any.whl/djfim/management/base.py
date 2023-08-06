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
# djfim.management.base

from ..runtime import DynamicBlock


class ENGINE(DynamicBlock):
    LABEL_ACTION_LOAD = 'LOAD'
    LABEL_ACTION_SAVE = 'SAVE'
    LABEL_ACTION_EXPORT = 'EXPORT'
    LABEL_ACTION_FIXUP = 'FIXUP'

    def getAction(self,  name):
        kls_ns = ['djfim','contrib','action',]
        kls_ns.append(name)
        act_kls = self.getDynClass('.'.join(kls_ns))
        return act_kls


class CONTEXT(DynamicBlock):
    CLASS_SORT_SOLVER = 'djfim.contrib.relation.sortedRelation'
    CLASS_DIGEST_SOLVER = 'djfim.contrib.notary.DigestSolver'
    CLASS_IMPRINT_SOLVER = 'djfim.contrib.notary.ImprintSolver'
    CLASS_ACTION_CACHE = 'djfim.function.QueueCache'
    CLASS_ARCHIVER = 'djfim.contrib.extraction.Archiver'
    CLASS_EXTRACT_ACTOR = 'djfim.contrib.extraction.Extractor'

    def getSortSolver(self):
        kls = self.getDynClass(self.CLASS_SORT_SOLVER)
        return kls(context=self)

    def getEntityCatalog(self):
        return NotImplementedError('virtual method')

    def getExtractor(self, label):
        kls = self.getDynClass(self.CLASS_EXTRACT_ACTOR)
        obj = kls(context=self)
        obj.data_model_name = label
        return obj

    def getActionCache(self):
        kls = self.getDynClass(self.CLASS_ACTION_CACHE)
        return kls(context=self)

    def getArchiver(self):
        kls = self.getDynClass(self.CLASS_ARCHIVER)
        return kls(context=self)

    def getDigestSolver(self):
        return self.getDynClass(self.CLASS_DIGEST_SOLVER)

    def getImprintSolver(self):
        return self.getDynClass(self.CLASS_IMPRINT_SOLVER)
