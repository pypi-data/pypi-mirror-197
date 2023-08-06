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
# djfim.settings

from django.test.signals import setting_changed
from dsgen import DSetting


class DjFIMSetting(DSetting):
    '''
    setting provider
    '''

    SETTING_NAME = 'DJFIM'

    DEFAULT = {
        'STORE': {
            'BLOB': '',
            'ENTITY': '',
            'GENERATION': '',
            'TRACK': '',
        },
        'SOLVER': {
            'MODEL': 'djfim.solver.DMSolver',
            'DEPENDENCY': 'djfim.solver.DependencySolver',
        },
    }

    def get_passthrough_fields(self):
        fields = []
        return fields
    pass


dm_setting = DjFIMSetting()

setting_changed.connect(dm_setting.signal_handler_setting_changed)
