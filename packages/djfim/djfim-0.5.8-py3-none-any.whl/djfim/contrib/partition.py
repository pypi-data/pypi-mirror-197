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
# djfim.contrib.partition

from collections import deque
from django.db import models
from ..function import LinearAlignment
from ..runtime import DynamicBlock


class PACK(object):

    CLASS_DATAMODEL_SOLVER  = 'djfim.solver.DMSolver'

    def __init__(self, data, altName=None):
        super().__init__()
        self.load_preset()
        self._data = data
        self._alternative_name = altName

    def load_preset(self):
        _loader = DynamicBlock()
        kls = _loader.getDynClass(self.CLASS_DATAMODEL_SOLVER)
        self.dm_solver = kls()

        self.storage_anchor_field = 'anchor'
        self.storage_label_field = 'model_name'
        self.storage_pk_field = 'id'
        return self

    @property
    def name(self):
        rval = self._alternative_name
        try:
            obj = self.content[0]
            rval = getattr(obj, self.storage_label_field)
        except:
            pass
        return rval

    @property
    def content(self):
        return self._data

    def __len__(self):
        return len(self.content)

    def __getitem__(self, index):
        return self.content[ index ]

    def get(self, anchor):
        pick_arg = {
            self.storage_anchor_field: anchor,
        }
        return self.content.get(**pick_arg)


class PackSolver(DynamicBlock):
    CLASS_PACK = 'djfim.contrib.partition.PACK'

    def __init__(self, head):
        super().__init__()
        self.load_preset()
        self._head = head

    def load_preset(self):
        self._pack_kls = self.getDynClass(self.CLASS_PACK)
        self.pack_label_attr = 'model_name'
        return self

    def get_select_arg(self, name):
        d = {
            self.pack_label_attr: name,
        }
        try:
            d = self._head.pool.getPartitionArguments(name)
        except:
            pass
        return d

    def getPack(self, name):
        collection = self._head.getCollection()
        select_arg = self.get_select_arg(name)
        data = collection.filter(**select_arg)
        return self._pack_kls(data, altName=name)


class LabelAlignment(LinearAlignment):

    def __init__(self, a:list, b:list):
        assert len(a) * len(b) > 0, 'invalid input'
        super().__init__(a, b)

    def load_preset(self):
        super().load_preset()
        self.Pos = DynamicBlock().getDynClass('djfim.function.Pos')

        self._row_cnt = len(self._b) + 1
        self._col_cnt = len(self._a) + 1

        self._xcnt = self._row_cnt * self._col_cnt
        self._mat = [0,] * self._xcnt

        self.item_label_attr = 'label'
        return self

    def getItemLabel(self, item):
        return getattr(item, self.item_label_attr, item)

    def getPos(self, index:int):
        row, col = divmod(index, self._col_cnt)
        pair = self.Pos(row=row, col=col)
        return pair

    def getIndex(self, pos) -> int:
        rval = pos.row * self._col_cnt + pos.col
        return rval

    def getPrior(self, pos) -> tuple:
        if (pos.row * pos.col) == 0:
            # special case: starting point (top-left) and edges;
            (prev_top, prev_left, prev_diag) = (0, 0, 0)
        else:
            prev_top  = self._mat[ self.getIndex( self.Pos(pos.row - 1, pos.col) ) ]
            prev_left = self._mat[ self.getIndex( self.Pos(pos.row, pos.col - 1) ) ]
            prev_diag = self._mat[ self.getIndex( self.Pos(pos.row - 1, pos.col - 1) ) ]
        return (prev_top, prev_left, prev_diag)

    def calculate(self, pos) -> tuple:
        if (pos.row * pos.col) == 0:
            # special case: two leading edges;
            (cost_top, cost_left, cost_diag) = (0, 0, 0)
        else:
            cost_top =  self.COST_SKIP
            cost_left = self.COST_SKIP

            a_item = self._a[ pos.col - 1 ]
            b_item = self._b[ pos.row - 1 ]
            if self.getItemLabel(a_item) == self.getItemLabel(b_item) :
                cost_diag = self.COST_EQUAL
            else:
                cost_diag = self.COST_MISS
        (prev_top, prev_left, prev_diag) = self.getPrior(pos)
        return (prev_top+cost_top, prev_left+cost_left, prev_diag+cost_diag)

    def do(self):
        # a) populate the matrix;
        for i in range(self._row_cnt):
            for j in range(self._col_cnt):
                pos = self.Pos(row=i, col=j)
                # get the best choice for current position;
                self._mat[ self.getIndex(pos) ]  = max(self.calculate(pos))

        # b) trace the best solution;
        step_cache = deque()
        i, j = ( self._row_cnt - 1, self._col_cnt -1 )

        while i + j > 0:
            pos = self.Pos(row=i, col=j)
            flag = [ (x == self._mat[ self.getIndex(pos) ]) for x in self.calculate(pos) ]
            # sanitize for edges;
            if 1 == i and j > 0:
                flag[ self.LABEL_PREV_CELL.index('T') ] = False
            elif 1 == j and i > 0:
                flag[ self.LABEL_PREV_CELL.index('L') ] = False

            bearing = self.LABEL_PREV_CELL[ flag.index(True) ]
            step_cache.appendleft(bearing)
            if 'L' == bearing:
                j -= 1
            if 'T' == bearing:
                i -= 1
            if 'D' == bearing:
                i -= 1
                j -= 1

        # fix the head step due to the sorting in LABEL_PREV_CELL;
        b_step = sum([ 1 for x in step_cache if x in ('T', 'D') ])
        a_step = sum([ 1 for x in step_cache if x in ('L', 'D') ])
        assert a_step <= (self._col_cnt - 1), 'abort'
        if b_step > (self._row_cnt - 1):
            step_cache.popleft()
            step_cache.appendleft('L')

        # c) formulate the per-series allocation;
        self.output = list()
        i, j = (0, 0)
        for step in step_cache:
            if 'D' == step:
                pair = (
                    self._a[j],
                    self._b[i],
                )
                i += 1
                j += 1
            if 'L' == step:
                pair = (
                    self._a[j],
                    self._blank,
                )
                j += 1
            if 'T' == step:
                pair = (
                    self._blank,
                    self._b[i],
                )
                i += 1
            self.output.append(pair)
        return self

    def __str__(self):
        SEP = '\t'
        cache = list()
        for i in range(self._row_cnt):
            line = list()
            for j in range(self._col_cnt):
                line.append(str(self._mat[ self.getIndex(self.Pos(i, j)) ]))
            cache.append(SEP.join(line))
        return '\n'.join(cache)


class Alignment(LinearAlignment):

    def load_preset(self):
        super().load_preset()
        self.output = list()
        self._profile = dict([ (k, 0) for k in self.LABEL_PREV_CELL ])

        self.item_label_attr = 'anchor'
        return self

    def _record_label(self, label):
        self._profile[ label ] = 1 + self._profile[ label ]
        return self

    def getLabelRange(self, qset):
        d = qset.aggregate(
            models.Min(self.item_label_attr, default=-1),
            models.Max(self.item_label_attr, default=-1)
        )

        k_min = '{f}__min'.format(
            f=self.item_label_attr
        )
        k_max = '{f}__max'.format(
            f=self.item_label_attr
        )
        return (d[ k_min ], d[ k_max ])

    def findRange(self):
        a_range = self.getLabelRange(self.unpack(self._a))
        b_range = self.getLabelRange(self.unpack(self._b))
        self.combined_range = (
            min([ x for x in ( a_range[0], b_range[0] ) if x > -1 ]),
            max([ x for x in ( a_range[1], b_range[1] ) ]),
        )
        assert self.combined_range[1] > 0, 'empty'
        return self

    def checkItemExistance(self, pack, itemID):
        lookup_arg = {
            self.item_label_attr: itemID,
        }
        content = self.unpack(pack)
        return content.filter(**lookup_arg).exists()

    def getVacancy(self):
        for index in range(self.combined_range[0], self.combined_range[1] + 1):
            offset = 0
            a_index = self._blank
            b_index = self._blank

            if self.checkItemExistance(self._a, index):
                offset += 1
                a_index = index
            if self.checkItemExistance(self._b, index):
                offset += 2
                b_index = index

            if offset == 0:
                # skip when both side are all empty;
                continue
            the_label = self.LABEL_PREV_CELL[ offset - 1 ]
            self._record_label(the_label)
            flag = (
                the_label,
                a_index,
                b_index,
            )
            self.output.append(flag)
        return self

    def do(self):
        self.findRange()
        self.getVacancy()
        return self

    def __str__(self):
        return ','.join([ f[0] for f in self.output ])
