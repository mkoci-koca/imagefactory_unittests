#!/usr/bin/env python
# encoding: utf-8

#   Copyright 2011 Red Hat, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#        Unit test for Image Factory test plan https://tcms.engineering.redhat.com/case/122789/?from_plan=4953
#        Created by koca (mkoci@redhat.com)
#        Date: 23/11/2011
#        Modified: 02/12/2011

import unittest
import logging
from imgfac.qmfagent.ImageFactory import ImageFactory

class testStatuses(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.NOTSET, format='%(asctime)s %(levelname)s %(name)s pid(%(process)d) Message: %(message)s', filename='/tmp/imagefactory-unittests.log')
        self.module_name01 = "BuildAdaptor"
        self.imagefactory = ImageFactory()
        self.object_statesBuildAdaptor = dict(states=str({
                                                          "NEW":({"INITIALIZING":("build_image", "push_image")}, {"PENDING":("build_image", "push_image")}, {"FAILED":("build_image", "push_image")}),
                                                          "INITIALIZING":({"PENDING":("_auto_")}, {"FAILED":("_auto_")}),
                                                          "PENDING":({"FINISHING":("_auto_")}, {"COMPLETED":("_auto_")}, {"FAILED":("_auto_")}),
                                                          "FINISHING":({"COMPLETED":("_auto_")}, {"FAILED":("_auto_")}),
                                                          "COMPLETED":()
                                                          }))
        #self.object_states
        self.maxDiff = None

    def tearDown(self):
        del self.module_name01
        del self.imagefactory
        del self.object_statesBuildAdaptor

    def testStatus(self):
        self.assertEqual(self.object_statesBuildAdaptor, self.imagefactory.instance_states(self.module_name01))
        

if __name__ == '__main__':
    unittest.main()
