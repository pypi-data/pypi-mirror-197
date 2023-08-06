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
# djfim.contrib.depot

from ..depository import POOL as _POOL, SPACE as _SPACE
from ..runtime import DynamicBlock


class Pool(_POOL):
    '''
    static data object
    '''

    CLASS_GENERATION = 'djfim.contrib.concrete.Generation'
    CLASS_ENTITY     = 'djfim.contrib.concrete.Entity'
    CLASS_LINKAGE    = 'djfim.contrib.depot.Linkage'
    CLASS_DIFF_SOLVER = 'djfim.contrib.diff.DiffScanner'

    def getAHead(self):
        head = None
        try:
            obj = self.STATE_DM.objects.filter(
                imprint__isnull=True
            ).order_by(
                'time_stamp'
            ).last()
            head = self.getGeneration(obj)
        except:
            pass
        return head

    def getBHead(self):
        head = None
        try:
            obj = self.STATE_DM.objects.filter(
                imprint__isnull=False
            ).order_by(
                'time_stamp'
            ).last()
            head = self.getGeneration(obj)
        except:
            pass
        return head

    def getCollection(self, head):
        qset = self.getInternalLinkage().getSet(head)
        return qset

    def getGeneration(self, obj):
        kls = DynamicBlock().getDynClass(self.CLASS_GENERATION)
        return kls(obj, pool=self)

    def getEntity(self, obj):
        kls = DynamicBlock().getDynClass(self.CLASS_ENTITY)
        return kls(obj)

    def getInternalLinkage(self):
        kls = DynamicBlock().getDynClass(self.CLASS_LINKAGE)
        return kls(parent=self)

    def addHead(self, data, aHead=None, bHead=None):
        obj = self.STATE_DM(**data)
        obj.save()
        head = self.getGeneration(obj)

        # link up;
        if aHead:
            #assert head.timestamp >= aHead.timestamp, 'no backdate'
            head.setLink(head.LABEL_LINK_A, aHead.storage_pk, True)
        if bHead:
            #assert head.timestamp >= bHead.timestamp, 'no backdate'
            head.setLink(head.LABEL_LINK_B, bHead.storage_pk, True)
        head.doSave()
        # maybe more generic, but it does not force the derivative to have the specific fields;
        return head

    def addEntity(self, data):
        obj = self.BLOB_DM(**data)
        obj.save()
        return self.getEntity(obj)

    def getDiffSolver(self):
        kls = DynamicBlock().getDynClass(self.CLASS_DIFF_SOLVER)
        return kls

    def getPartitionArguments(self, label):
        arg = {
            'model_name': label,
        }
        return arg


class Linkage(DynamicBlock):
    '''
    internal link encapsulation
    '''

    def __init__(self, parent):
        assert parent is not None, 'invalid value'
        super().__init__()
        self._parent = parent

    @property
    def BLOB_DM(self):
        return self._parent.BLOB_DM

    def get_lookup_arg(self, head):
        d = dict()
        d['entity__generation_id'] = head.storage_pk
        return d

    def getBackingSet(self):
        qset = tuple()
        try:
            qset = self.BLOB_DM.objects.filter(
                **(self._lookup_arg)
            ).distinct()
        except:
            pass
        return qset

    def getSet(self, head):
        self._lookup_arg = self.get_lookup_arg(head)
        return self.getBackingSet()


class WorkSpace(_SPACE):
    '''
    space of live data object
    '''

    CLASS_DATAMODEL_SOLVER = 'djfim.solver.DMSolver'
    CLASS_URI_PARSER = 'djfim.contrib.schema.URIParser'
    CLASS_OBJECT_OPERATOR  = 'djfim.contrib.depot.ObjectPersistence'

    def __init__(self):
        super().__init__()
        self.load_preset()

    def load_preset(self):
        self.dm_solver = DynamicBlock().getDynClass(self.CLASS_DATAMODEL_SOLVER)()
        self.uri_solver_kls = DynamicBlock().getDynClass(self.CLASS_URI_PARSER)

        self.obj_operator_kls = DynamicBlock().getDynClass(self.CLASS_OBJECT_OPERATOR)
        self.storage_pk_field = 'id'
        return self

    def get_live_object(self,  uri):
        '''
        :param uri: (string)
        '''
        obj = None

        d = self.uri_solver_kls().parseURI(uri)
        try:
            pick_arg = {
                self.storage_pk_field: d['anchor'],
            }
            obj = self.dm_solver.get_model_class(
                d['app_label'],
                d['model_name']
            ).objects.get(**pick_arg)
        except:
            pass
        return obj

    def getObjectOperator(self):
        return self.obj_operator_kls(self)


class ObjectPersistence(DynamicBlock):
    '''
    persist the changes to live objects
    '''

    DEPENDENCY_MAP_KEY = '{dm}={pk}'

    CLASS_DATAMODEL_SOLVER = 'djfim.solver.DMSolver'
    CLASS_DEPENDENCY_SOLVER = 'djfim.solver.DependencySolver'
    CLASS_PACK_SOLVER  = 'djfim.contrib.partition.PackSolver'
    CLASS_CONTENT_LOADER = 'djfim.contrib.schema.toDict'

    ATTRIBUTE_FIELD_LIST = (
        'django.db.models.BooleanField',
        'django.db.models.FloatField',
        'django.db.models.IntegerField',
    )

    def __init__(self, wspace):
        assert wspace is not None, 'invalid input'
        super().__init__()
        self.load_preset()
        self._wspace = wspace

    def load_preset(self):
        self._pack_solver_kls = self.getDynClass(self.CLASS_PACK_SOLVER)
        self._content_loader_kls = self.getDynClass(self.CLASS_CONTENT_LOADER)
        self._fk_solver_kls = self.getDynClass(self.CLASS_DEPENDENCY_SOLVER)
        self._dependency_cache_kls = dict

        self._attr_field_list = tuple([ self.getDynClass(kls) for kls in self.ATTRIBUTE_FIELD_LIST ])
        self.dm_solver = self.getDynClass(self.CLASS_DATAMODEL_SOLVER)()
        self._context = None
        return self

    def setContext(self, context):
        assert context is not None, 'invalid input'
        self._context = context
        return self

    def updateSpace(self, item):
        live_obj = self._wspace.get_live_object(item.uri)
        if live_obj is None:
            self.createNewObject(item)
        else:
            self.updateLiveObject(live_obj, item)
        return self

    def updateLiveObject(self, obj, item):
        d = self.extract(item, dm=obj.__class__)
        for k, v in d:
            if k in (self._wspace.storage_pk_field,):
                continue
            setattr(obj, k, v)
        obj.save()
        return self

    def createNewObject(self, item):
        uri = self._wspace.uri_solver_kls().parseURI(item.uri)
        obj_dm = self.dm_solver.get_model_class(
            uri['app_label'],
            uri['model_name']
        )

        raw = self.extract(item, dm=obj_dm)
        new_obj = obj_dm(**raw)
        new_obj.save()

        # store the new anchor value and add to cache;
        premap_reference = self.DEPENDENCY_MAP_KEY.format(
            dm=item.obj_kls,
            pk=item.anchor
        )
        setattr(item._obj, 'anchor', new_obj.id)
        item.doSave()
        self._dependency_cache[ premap_reference ] = new_obj.id
        return self

    def getSortedItem(self):
        for name in self.sorted_pack_name:
            pack = self.pack_solver.getPack(name)
            for item in pack.content:
                yield item

    def extract(self, entity, dm):
        d = dict()
        loader = self._content_loader_kls(entity.toBIEF().splitlines())
        d.update(loader.dict)
        d.pop('dn')

        d = self.normalizeAttribute(d, dm)
        d = self.normalizeRelation(d, dm)
        return d

    def normalizeRelation(self, data, dm):
        fk_solver = self._fk_solver_kls(dm)
        fk_target_list = fk_solver.get_target_list()

        for fk in fk_target_list:
            if fk_solver.accept(fk):
                key_name = fk.name + '_id'

                premap_value = data.pop(fk.name, None)
                if premap_value is None:
                    continue
                premap_value = fk.to_python(
                    self._wspace.uri_solver_kls().parseURI(premap_value)['anchor']
                )

                if fk_solver.reject(fk):
                    if fk.related_model._meta.label != dm._meta.label:
                        data[ key_name ] = getattr(self._context, 'FALLBACK_USER_ID', 1)
                    else:
                        data[ key_name ] = premap_value
                else:
                    # patch with dependency cache;
                    premap_target = self.DEPENDENCY_MAP_KEY.format(
                        dm=fk.related_model._meta.label,
                        pk=premap_value
                    )
                    # if referencing an existing record, the cache lookup may fail, then use the original value;
                    mapped_value = self._dependency_cache.get(
                        premap_target,
                        premap_value
                    )
                    data[ key_name ] = mapped_value
        return data

    def normalizeAttribute(self, data, dm):
        for f in dm._meta.fields:
            try:
                assert f.name != self._wspace.storage_pk_field, 'skip'
                val = data[ f.name ]
                if isinstance(f, self._attr_field_list):
                    data[ f.name ] = f.to_python(val)
            except (AssertionError, KeyError):
                pass
        return data

    def castToEntity(self, obj):
        return self._pool.getEntity(obj)

    def do(self, head, hint):
        self._head = head
        self._hint = hint

        self._dependency_cache = self._dependency_cache_kls()
        self.sorted_pack_name = self._context.getSortSolver().get()
        self.pack_solver = self._pack_solver_kls(self._head)

        for item in self.getSortedItem():
            self.updateSpace(self.castToEntity(item))
        return self
