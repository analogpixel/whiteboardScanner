#!/usr/bin/env python
#
# class to send and retrieve files from s3

import boto3

class s3Con:
    def __init__(self):
        self.s3 = boto3.client('s3',
                               aws_access_key_id="KEY",
                               aws_secret_access_key="KEYPASS",
                               region_name='us-west-2')

    def upload(self, fileName, roomName='Default'):
        self.s3.upload_file("cache/" + fileName, "whiteboardscan", roomName + "/" + fileName)

    def listFiles(self, roomName='Default'):
        print( self.s3.list_objects(Bucket='whiteboardscan', Prefix= roomName + "/" ) )
        return self.s3.list_objects(Bucket='whiteboardscan', Prefix= roomName + "/" )['Contents']
    
