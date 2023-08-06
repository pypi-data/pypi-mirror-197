# Copyright 2015 0xc0170
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

from unittest import TestCase

from project_generator_definitions.definitions import ProGenDef

class TestDefinitions(TestCase):

    """test things related to ProjGenDef class"""

    def setUp(self):
        self.definitions = ProGenDef('novalid')

    # def test_get_mcu_def(self):
    #     mcu_def = self.definitions.get_mcu_definition()
    #     # not empty dic return
    #     assert bool(mcu_def)
    #     assert mcu_def['mcu']['vendor']
    #     assert mcu_def['mcu']['name']
    #     assert mcu_def['mcu']['core']

    def test_get_targets(self):
        target = self.definitions.get_targets()
        # it's not empty list as we got some targets
        assert bool(target)

    def test_get_mcu_core(self):
        # valid target
        core = self.definitions.get_mcu_core('frdm-k64f')
        assert core != None
        assert core[0] == 'cortex-m4f'
        core = self.definitions.get_mcu_core('novalid')
        assert core == None

    def test_tool_def(self):
        tool_def = self.definitions.get_tool_definition('novalid')
        assert tool_def == None

    def test_is_supported(self):
        supported = self.definitions.is_supported('novalid')
        supported == False

