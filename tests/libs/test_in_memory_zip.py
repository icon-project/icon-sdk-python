# -*- coding: utf-8 -*-
# Copyright 2018 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os import path
from unittest import TestCase, main

from iconsdk.libs.in_memory_zip import gen_deploy_data_content


class TestInMemoryZip(TestCase):

    def test_in_memory_zip(self):
        current_dir_path = path.abspath(path.dirname(__file__))
        score_path = path.join(current_dir_path, 'sample_token')
        tests_path = path.join(current_dir_path, 'sample_token','tests')
        # bytes of sample_token's content
        content_bytes = gen_deploy_data_content(score_path)
        content_bytes_as_str = str(content_bytes)
        self.assertFalse('test_integrate_sample_token.py' in content_bytes_as_str )
        self.assertFalse(tests_path[1:] in content_bytes_as_str)
        self.assertTrue(score_path[1:] in content_bytes_as_str)


if __name__ == "__main__":
    main()
