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
# djfim.runtime

import logging
import traceback

from django.utils.module_loading import import_string


class BLOCK(object):

    def getLogger(self):
        logger = logging.getLogger(self.LOG_NAME)
        return logger


class STACKTRACE(object):

    def get(self):
        return traceback.format_exc()


class DynamicBlock(BLOCK):

    def getDynClass(self, name):
        kls = None
        try:
            kls = import_string(name)
        except:
            self.getLogger().debug(STACKTRACE().get())
        return kls
