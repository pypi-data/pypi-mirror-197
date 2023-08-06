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
# djfim.function

import base64
from collections import deque
import json
from typing import NamedTuple


def no_translations(f):
    def inner(*args, **kwargs):
        return f(*args, **kwargs)
    return inner


class Codec(object):
    '''
    encode/decode helper
    '''

    def to_representation(self, obj):
        '''
        :param obj: (object)
        '''
        _json_obj = json.dumps(obj)
        rval = base64.b64encode(_json_obj.encode()).decode()
        return rval

    def to_python(self, x):
        '''
        :param x: (string)
        '''
        _json_string = base64.b64decode(x.encode()).decode()
        rval = json.loads(_json_string)
        return rval


class Pos(NamedTuple):
    row: int
    col: int


class LinearAlignment(object):
    '''
    generate sparse linear alignment
    '''

    COST_MISS  = -1
    COST_SKIP  = 1
    COST_EQUAL = 3  # COST_MATCH > 2 * COST_SKIP
    # cost function: match > inset > mismatch;
    LABEL_PREV_CELL = ( 'T', 'L', 'D', )

    def __init__(self, a, b):
        super().__init__()
        self._a = a
        self._b = b
        self.load_preset()

    def load_preset(self):
        self._blank = None
        return self

    def unpack(self, obj):
        return obj.content

    def getItemLabel(self, item):
        return item

    def do(self):
        return self


class QueueCache(deque):
    '''
    simple cache helper
    '''

    def __init__(self, context, parent=None):
        super().__init__()
        self._context = context
        self._parent = parent

    @property
    def context(self):
        return self._context

    @property
    def parent(self):
        return self._parent
