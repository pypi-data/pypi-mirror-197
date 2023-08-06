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
# djfim.contrib.relation

from ..runtime import DynamicBlock
from ..solver import SortSolver


class sortedRelation(SortSolver):

    DATAMODEL_SOLVER  = 'djfim.solver.DMSolver'
    DEPENDENCY_SOLVER = 'djfim.solver.DependencySolver'

    def __init__(self, context=None):
        super().__init__()
        self.load_preset()
        self._context = context

    def load_preset(self):
        _loader = DynamicBlock()

        self.dm_solver_cls = _loader.getDynClass(self.DATAMODEL_SOLVER)
        self.dm_solver = self.dm_solver_cls()

        self.relation_solver_cls = _loader.getDynClass(self.DEPENDENCY_SOLVER)

        return self

    def get(self):
        pack_set = self.get_workset()
        return self.get_stable_sort(pack_set)

    def get_workset(self):
        return self._context.getEntityCatalog()


class stubRelation(object):

    def __init__(self, related):
        super().__init__()
        self.related_model = related
