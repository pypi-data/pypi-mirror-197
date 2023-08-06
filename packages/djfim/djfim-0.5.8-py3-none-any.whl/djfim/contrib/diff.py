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
# djfim.contrib.diff

import json

from ..runtime import DynamicBlock


class SDIFF(object):
    SEP = '|'
    COL_NAMES = ['status', 'choice', 'uri', 'a', 'b']

    LABEL_ADD = 'A'
    LABEL_CHANGE = 'C'
    LABEL_DROP = 'D'

    def __str__(self):
        return json.dumps(self.asDict())

    def asDict(self):
        d = dict()
        for f in self.COL_NAMES:
            d[ f ] = str(getattr(self, f,  ''))
        return d

    @property
    def type(self):
        if self.a is None:
            return self.LABEL_ADD
        if self.b is None:
            return self.LABEL_DROP
        return self.LABEL_CHANGE


class DIFFBATCH(object):

    def __init__(self):
        super().__init__()
        self.load_preset()

    def load_preset(self):
        self._batch = list()
        return self

    def append(self, item):
        return self._batch.append(item)

    def __iter__(self):
        for item in self._batch:
            yield item

    def get(self, uri):
        obj = None
        for item in self._batch:
            if item.uri == uri:
                obj = item
                break
        return obj

    def getEntityStatus(self, uri):
        diff = self.get(uri)
        return diff.status

    def getEntityChoice(self, uri):
        diff = self.get(uri)
        return diff.choice


class DiffLoader(DynamicBlock):
    CLASS_DIFF = 'djfim.contrib.diff.SDIFF'
    CLASS_BATCH = 'djfim.contrib.diff.DIFFBATCH'

    def __init__(self):
        super().__init__()
        self.load_preset()

    def load_preset(self):
        self._diff_kls = self.getDynClass(self.CLASS_DIFF)
        self._batch_kls = self.getDynClass(self.CLASS_BATCH)
        return self

    def loadFromString(self, content):
        cache = self._batch_kls()
        data = json.loads(content)
        cache.a_pk = data['_meta']['a']
        cache.b_pk = data['_meta']['b']
        for row in data['diff']:
            obj = self.parse_single_row(row)
            cache.append(obj)
        return cache

    def parse_single_row(self, line):
        obj = self._diff_kls()

        assert len(line.keys()) >= len(obj.COL_NAMES), 'invalid input'

        for field in obj.COL_NAMES:
            fval = line[ field ]
            setattr(obj, field, fval)

        return obj


class DiffScanner(DynamicBlock):
    CLASS_ENTITY_DIFF = 'djfim.contrib.diff.EntityDiff'

    CLASS_PACK_SOLVER  = 'djfim.contrib.partition.PackSolver'
    CLASS_ALIGN_SOLVER = 'djfim.contrib.partition.Alignment'

    def __init__(self, context, aHead, bHead):
        super().__init__()
        self.load_preset(context=context)
        #
        self._context = context
        self._a_head = aHead
        self._b_head = bHead

    def load_preset(self, context=None):
        self._pack_solver_cls = self.getDynClass(self.CLASS_PACK_SOLVER)
        self._entity_diff_cls = self.getDynClass(self.CLASS_ENTITY_DIFF)
        self._align_solver_cls = self.getDynClass(self.CLASS_ALIGN_SOLVER)
        self._dependency_cache_cls = dict

        try:
            ctx_diff_kls = self.getDynClass(context.CLASS_ENTITY_DIFF)
            assert ctx_diff_kls is not None, 'ignore empty value'
            self._entity_diff_cls = ctx_diff_kls
        except:
            pass
        return self

    def getPackPair(self):
        # a) get sorted;
        sorted_pack_name = self._context.getSortSolver().get()

        # b) collect packs;
        a_pak_solver = self._pack_solver_cls(self._a_head)
        b_pak_solver = self._pack_solver_cls(self._b_head)

        for name in  sorted_pack_name:
            a_pack = a_pak_solver.getPack(name)
            b_pack = b_pak_solver.getPack(name)
            yield (a_pack, b_pack)

    def getAlignedCollection(self, aSet, bSet):
        align = self._align_solver_cls(aSet, bSet)
        align.item_label_attr = 'anchor'
        return align.do().output

    def filterStatus(self, flag):
        rval = False
        if flag[0] in ('L', 'D'):
            rval = True
        return rval

    def filterDiff(self, item):
        rval = False
        try:
            if item.type in (item.LABEL_ADD, item.LABEL_CHANGE,):
                rval = True
        except:
            pass
        return rval

    def loadEntity(self, obj):
        # use b side to cast obj, because b side must exist in order to do diff;
        rval = None
        try:
            rval = self._b_head.pool.getEntity(obj)
        except:
            pass
        return rval

    def comparePack(self, aPack, bPack):
        pack_diff_cache = list()

        pack_status = self.getAlignedCollection(
            aPack,
            bPack
        )

        for flag in pack_status:
            if self.filterStatus(flag):
                entity_cmp = self._entity_diff_cls(
                    self.loadEntity(aPack.get(flag[1])),
                    self.loadEntity(bPack.get(flag[2])),
                    self._dependency_cache
                )
                # register any mapping in `self._dependency_cache`;
                pack_diff_cache.append(entity_cmp.get())

        return pack_diff_cache

    def getDiff(self, sink):
        self._dependency_cache = self._dependency_cache_cls()

        _work_cache = list()
        # a) get pack/partition on head;
        for each_pack in self.getPackPair():
        # b) scan within each pack;
            _work_cache.extend(
                self.comparePack(
                    each_pack[0],
                    each_pack[1]
                )
            )
        # c) concatenate rvalue;
        self.diff_cache = [ item for item in _work_cache if self.filterDiff(item) ]
        sink.extend(self.diff_cache)
        return self


class EntityDiff(DynamicBlock):
    CLASS_DIFF = 'djfim.contrib.diff.SDIFF'
    LABEL_CHOICE_ADD    = 'b'
    LABEL_CHOICE_CHANGE = 'b'
    LABEL_CHOICE_DROP   = 'a'

    def __init__(self, aEntity, bEntity, dependency):
        super().__init__()
        self.load_preset()
        #
        self._a_entity = aEntity
        self._b_entity = bEntity
        self._dependency = dependency

    def load_preset(self):
        self._diff_cls = self.getDynClass(self.CLASS_DIFF)
        return self

    def lookUpDependency(self, anchor, f):
        rval = None
        try:
            obj = self._dependency[ f ].get(anchor, None)
            rval = obj.anchor
        except:
            pass
        return rval

    def checkDiff(self):
        rval = True
        try:
            rval = not( self._a_entity.content == self._b_entity.content )
        except:
            pass
        return rval

    def constructDiff(self):
        diff = self._diff_cls()
        diff.a = None
        try:
            diff.a = self._a_entity.content
        except:
            pass
        diff.b = None
        try:
            diff.b = self._b_entity.content
        except:
            pass
        try:
            diff.uri = self._a_entity.uri
        except:
            diff.uri = self._b_entity.uri

        # set flag;
        diff.status = diff.LABEL_CHANGE
        diff.choice = self.LABEL_CHOICE_CHANGE
        if diff.a is None:
            diff.status = diff.LABEL_ADD
            diff.choice = self.LABEL_CHOICE_ADD
        if diff.b is None:
            diff.status = diff.LABEL_DROP
            diff.choice = self.LABEL_CHOICE_DROP
        return diff

    def get(self):
        obj = None
        if self.checkDiff():
            obj = self.constructDiff()
        return obj


class DiffActuator(DynamicBlock):
    CLASS_DIFF = 'djfim.contrib.diff.SDIFF'

    def __init__(self, aHead, bHead, diffSet, altPool=None):
        assert bHead is not None,  'invalid input'
        assert (aHead is not None) or (altPool is not None),  'invalid input'
        super().__init__()
        self.load_preset()
        #
        self._a_head = aHead
        self._b_head = bHead
        self._diff_set = diffSet
        self._alternative_pool = altPool

    def load_preset(self):
        self._diff_cls = self.getDynClass(self.CLASS_DIFF)
        self._dependency_cache_cls = dict
        return self

    def patchData(self, data, head):
        data['generation'] = head.storage_pk
        return data

    def applyDiff(self):
        # a) loop over existing ones;
        for entity in self._start:
            new_data = entity.copyAsDict()
            try:
                diff = self._diff_set.get(entity.uri)
                if diff.type == diff.LABEL_CHANGE:
                    if diff.choice == 'b':
                        new_data = self._b_head.lookUpEntity(entity.uri).copyAsDict()
            except:
                pass

            self._pool.addEntity(
                self.patchData(
                    new_data,
                    self._new_a_head
                )
            )

        # b) collect new ones;
        for diff in self._diff_set:
            if diff.type == diff.LABEL_ADD:
                add_data = self._b_head.lookUpEntity(diff.b_uri).copyAsDict()
                self._pool.addEntity(
                    self.patchData(
                        add_data,
                        self._new_a_head
                    )
                )
        return self

    def getHeadData(self):
        d = {
            'time_stamp': self._ts,
            'memo': 'combined node',
        }
        return d

    def do(self, now):
        self._ts = now
        # a) create new node;
        new_a_data = self.getHeadData()

        try:
            self._pool = self._a_head.pool
        except AttributeError:
            self._pool = self._alternative_pool

        self._new_a_head = self._pool.addHead(
            new_a_data,
            aHead=self._a_head,
            bHead=self._b_head
        )
        # b) loop through;
        self._start = self._a_head.getEntitySet()
        self.applyDiff()
        return self

    @property
    def latest_head(self):
        return self._new_a_head
