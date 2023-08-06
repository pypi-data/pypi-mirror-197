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
# djfim.shortcut

from .runtime import DynamicBlock
from .settings import dm_setting


class ShortcutFactory(DynamicBlock):

    def __init__(self):
        super().__init__()
        self.setting = dm_setting
        self.load_preset()

    def load_preset(self):
        self._slots = dict()
        return self

    def get_list(self):
        return self._slots.keys()

    def get_item(self, name):
        '''
        :param name: (string)
        '''
        rval = None
        try:
            mapped_name = self._slots[name]
            rval = self.getDynClass(mapped_name)
        except:
            pass
        return rval
    pass


__factory = ShortcutFactory()

__dir__ = __factory.get_list
__getattr__ = __factory.get_item
