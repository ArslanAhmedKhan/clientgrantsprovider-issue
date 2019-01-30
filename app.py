#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

#<< THIS SCRIPT IS GIVING ERRORS WITH STS ENABLED >>>>

import logging
import boto3

from botocore.session import get_session
from boto3.session import Session
from client_grants import ClientGrantsCredentialProvider

#boto3.set_stream_logger('boto3.resources', logging.DEBUG)
boto3.set_stream_logger('botocore', level='DEBUG')

bc_session = get_session()
#bc_session.get_component('credential_provider').insert_before(
#    'env',
#    ClientGrantsCredentialProvider('TQKS830EUY7A8I1GRIJV',
#                                   'JtKFlIk8IEccP+gorQAT9c+eggi+po55Zc+qjEoB'),
#)

bc_session.get_component('credential_provider').insert_before(
    'env',
    ClientGrantsCredentialProvider('minio',
                                   '504324a5-c601-45e9-813d-59462fa4102b'),
)

print("bc_session:",bc_session);
boto3_session = Session(botocore_session=bc_session)
print("boto3_session:", boto3_session);
s3 = boto3_session.resource('s3',endpoint_url='http://192.168.56.102:9000')
#s3 = boto3.resource('s3',endpoint_url='http://192.168.56.102:9000',config=boto3.session.Config(signature_version='s3v4'))
print("s3:>>>>>>>>>>>>>>>>>>>>",s3);

with open('/home/docker/mnt/data/arslan-bucket/token.json', 'rb') as data:
    s3.meta.client.upload_fileobj(data,
                                  'arslan-bucket',
                                  'token.json'#,                                  ExtraArgs={'ServerSideEncryption':'AES256'}
				  )

# Upload with server side encryption, using temporary credentials
#s3.meta.client.upload_file('/home/docker/mnt/data/arslan-bucket/token.json',
 #                          'arslan-bucket',
  #                         'token.json',
   #                        ExtraArgs={'ServerSideEncryption':'AES256'})

# Download encrypted object using temporary credentials
s3.meta.client.download_file('arslan-bucket', 'token.json', '/home/docker/mnt/tmp/data/arslan-bucket/token.json')
