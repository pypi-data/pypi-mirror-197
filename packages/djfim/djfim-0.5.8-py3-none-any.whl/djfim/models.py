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
# djfim.models

from django.db import models


_ANCHOR_NUM_FIELD = models.PositiveBigIntegerField


class Blob(models.Model):
    content = models.TextField(null=True)
    digest = models.TextField(null=True)

    class Meta:
        abstract = True


class Entity(models.Model):
    app_label  = models.CharField(max_length=128)
    model_name = models.CharField(max_length=128)
    anchor = _ANCHOR_NUM_FIELD()

    series = models.PositiveBigIntegerField()

    class Meta:
        abstract = True


class Generation(models.Model):
    time_stamp = models.DateTimeField()
    memo = models.TextField(null=True)
    digest = models.TextField(null=True)
    imprint = models.TextField(null=True)

    class Meta:
        abstract = True


class Caret(models.Model):
    name = models.CharField(max_length=256)
    memo = models.TextField(null=True)
    digest = models.TextField(null=True)

    class Meta:
        abstract = True
