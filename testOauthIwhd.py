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
#        Unit test for Image Factory test plan https://tcms.engineering.redhat.com/case/122798/?from_plan=4953
#        Created by koca (mkoci@redhat.com)
#        Date: 25/11/2011
#        Modified: 02/12/2011

import unittest2
import logging
from imgfac.ImageWarehouse import ImageWarehouse
from imgfac.ApplicationConfiguration import ApplicationConfiguration
import oauth2 as oauth
import httplib2
#import time

class testOauthIwhd(unittest2.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.NOTSET, format='%(asctime)s %(levelname)s %(name)s pid(%(process)d) Message: %(message)s', filename='/tmp/imagefactory-unittests.log')
        self.warehouse = ImageWarehouse(ApplicationConfiguration().configuration["warehouse"])
        self.warehouseKey = self.warehouse.warehouse_credentials['key'] if self.warehouse.warehouse_oauth else 'warehousekey'
        self.warehouseSecret = self.warehouse.warehouse_credentials['secret'] if self.warehouse.warehouse_oauth else 'warehousesecret'

    def tearDown(self):
        del self.warehouseKey
        del self.warehouse
        del self.warehouseSecret

    def testOauthIwhd(self):
        #querying iwhd;
        #https://www.aeolusproject.org/redmine/projects/aeolus/wiki/OAuth
        consumer = oauth.Consumer(key=self.warehouseKey,secret=self.warehouseSecret)
        sig_method = oauth.SignatureMethod_HMAC_SHA1()
        oauth_version = None
        try:
            oauth_version = oauth.OAUTH_VERSION
        except AttributeError:
            oauth_version = oauth.VERSION
        params = {'oauth_version':oauth_version,
                  'oauth_nonce':oauth.generate_nonce(),
                  'oauth_timestamp':oauth.generate_timestamp(),
                  'oauth_signature_method':sig_method.name,
                  'auth_consumer_key':consumer.key}
        req = oauth.Request(method='GET', url=self.warehouse.url, parameters=params)
        sig = sig_method.signing_base(req, consumer, None)
        #print "\n" 
        #print sig
        req['oauth_signature'] = sig
        r, c = httplib2.Http().request(self.warehouse.url, 'GET', None, headers=req.to_header())
        #print '\nResponse headers: %s\nContent: %s' % (r,c)
        self.assertIsNotNone(c)
        self.assertIsNotNone(r)
        #self.warehouse._oauth_headers(self.warehouse.url, 'GET')
        #self.assert_(self.warehouse.create_bucket_at_url("%s/unittests-create_bucket/%s" % (self.warehouse.url, "unittest-koca")))
        
        
    def testStoreTemplate(self):
        # TEMPLATE
        template_content = "<template>This is a test template.</template>"
        # store the template and let an id get assigned
        template_id = self.warehouse.store_template(template_content)
        self.assertIsNotNone(template_id)
        

if __name__ == '__main__':
    unittest2.main()
