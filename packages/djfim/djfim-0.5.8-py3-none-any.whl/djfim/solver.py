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
# djfim.solver

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.topological_sort import stable_topological_sort


class DMSolver(object):

    def get_model_class(self, app_label, model_name=None):
        '''
        :param app_label: (string)
        :param model_name: (string)

        :return: (object reference)
        '''
        mod = apps.get_model(app_label, model_name)
        return mod

    def get_unique_label(self, obj):
        '''
        :param obj: (object)

        :return: (string)
        '''
        return obj._meta.label


class SortSolver(object):

    def get_relation_target_list(self, item):
        '''
        :param item: (object)
        '''
        dm = self.dm_solver.get_dm(item)
        relation_solver = self.relation_solver_cls(dm)
        return relation_solver.get_dependency()

    def get_stable_sort(self, workset):
        '''
        :param workset: (iterable)

        :return: (list)
        '''
        g = dict()
        for each in workset:
            dependency = self.get_relation_target_list(each)
            vset = set()
            for f in dependency:
                fm = self.dm_solver.get_unique_label(f.related_model)
                vset.add(fm)
            g[ each ] = vset
        return stable_topological_sort(g.keys(), g)


class DependencySolver(object):

    def __init__(self, dm):
        '''
        :param dm: (model)
        '''
        super().__init__()
        self.dm = dm
        #
        self.load_preset()

    def load_preset(self):
        '''
        populate essential attributes: `d_types`, `user_dm`, `masked_t`
        '''
        self.d_types = (
            models.ForeignKey,
            models.OneToOneField,
        )

        self.user_dm = get_user_model()
        self.masked_t = (
            self.dm._meta.label,
            self.user_dm._meta.label,
        )
        return self

    def get_target_list(self):
        return self.dm._meta.fields

    def accept(self, f):
        '''
        :param f: (field)

        :return: (boolean)
        '''
        rval = isinstance(f, self.d_types)
        return rval

    def reject(self, f):
        '''
        skip self-referencing link or known target set;

        :param f: (field)

        :return: (boolean)
        '''
        rval = ( f.related_model._meta.label in self.masked_t )
        return rval

    def posthook(self, fs):
        '''
        post-processing hook

        :param f: (set)

        :return: (set)
        '''
        return fs

    def get_dependency(self):
        '''
        :return: (set)
        '''
        t = set()
        field_list = self.get_target_list()
        for f in field_list:
            if self.accept(f):
                if self.reject(f):
                    continue
                t.add(f)
        return self.posthook(t)
