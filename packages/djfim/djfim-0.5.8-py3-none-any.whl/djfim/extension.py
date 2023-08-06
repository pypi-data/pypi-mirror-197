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
# djfim.extension


class Imprint(object):

    def do(self, stream):
        raise NotImplementedError('virtual method')


class SaltedImprint(Imprint):

    def do(self, stream):
        ret = None

        try:
            import os
            keyid = os.getenv('DJFIM_IMPRINT_KEY', None)
            salt = os.getenv('DJFIM_IMPRINT_SALT', '')
            assert keyid is not None, 'skip'
            full_raw = '{a}{b}'.format(
                a=stream,
                b=salt
            ).encode()
            import gpg
            with gpg.Context(armor=True) as _c:
                key = _c.get_key(keyid)
                with gpg.Context(armor=True, signers=[key]) as _cx:
                    ret, unused_val = _cx.sign(
                        full_raw,
                        mode=gpg.constants.sig.mode.DETACH,
                    )
        except:
            pass
        return ret
