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
# djfim.base

from dmprj.concept.structural.versioned import Entity as _ENTITY, Snapshot as _STATE


class ENTITY(_ENTITY):

    @property
    def uri(self):
        return NotImplementedError('virtual method')

    @property
    def content(self):
        return NotImplementedError('virtual method')

    @property
    def digest(self):
        '''
        :return: (string)
        '''
        return NotImplementedError('virtual method')


class GENERATION(_STATE):

    @property
    def timestamp(self):
        return NotImplementedError('virtual method')

    @property
    def memo(self):
        return NotImplementedError('virtual method')

    @property
    def digest(self):
        return NotImplementedError('virtual method')

    @property
    def imprint(self):
        return NotImplementedError('virtual method')


class BasePolicy(object):
    '''
    base-class of policy provider
    '''

    def accept(self, instance):
        raise NotImplementedError('virtual method')

    def reject(self, instance):
        raise NotImplementedError('virtual method')
