"""
  Description:    Awss3 client
"""

import os
import logging

import boto3
import botocore
from core.general import settings
from core.general.exceptions import SIDException


class AwsS3Client():
    """
        The class responsiblities are:
            Setup connection with Aws S3 and fetch the records
    """

    def __init__(self, *args, **kwargs):
        self.write_permission = None
        self.session = None
        self.s3 = None
        self.s3_bucket = None
        self.bucket_name = None
        self.s3objects = []

    def authenticate(self,
                     aws_access_key_id,
                     aws_secret_access_key,
                     bucket_name,
                     aws_region
                     ):
        """
            get authentication setup
        """
        try:
            self.session = boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )
            self.s3 = self.session.resource('s3')
            self.s3_bucket = self.s3.Bucket(bucket_name)
            _ = self.s3_bucket.meta.client.head_bucket(
                Bucket=bucket_name)
            self.bucket_name = bucket_name
            # if self.s3 is None:
            #     raise SIDException('Connection error')
        except botocore.exceptions.ClientError as err:
            logging.error(str(err))
            self.session = None
            self.s3 = None
            self.s3_bucket = None
            raise SIDException("Aws S3 Connection Error")

        except Exception as err:
            logging.error(str(err))
            logging.error(str(self.session))
            self.session = None
            self.s3 = None
            self.s3_bucket = None
            raise SIDException("Aws S3 Connection Error")

    def getclient(self, connector):
        """
            get connection details
        """
        from core.models.coreproxy import AuthAwsS3Proxy
        auth_record = AuthAwsS3Proxy.objects.get_or_none(
            conn_object_id=connector.object_id
        )
        if not auth_record:
            raise SIDException('auth client missing', 'S3')
        """
            decrypt the data
        """
        from core.general.sidcrypt import SIDEncryption

        sid_crypt = SIDEncryption()
        aws_access_key_id = sid_crypt.decrypt(auth_record.aws_access_key_id)
        aws_secret_access_key = sid_crypt.decrypt(
            auth_record.aws_secret_access_key)
        self.authenticate(
            aws_access_key_id,
            aws_secret_access_key,
            auth_record.bucket_name,
            auth_record.aws_region
        )

    def getallfiles(self):
        """
            get all file details
        """
        for s3_file in self.s3_bucket.objects.all():
            record = {
                's3_file': s3_file,
                'key': s3_file.key
            }
            self.s3objects.append(record)

    def fetchfilefromkey(self, filekey=None):
        """
            get file details
        """
        if not filekey:
            return None

        file_name = os.path.basename(str(filekey))
        dest_file = settings.DOCUMENT_PATH + file_name
        try:
            self.s3_bucket.download_file(filekey, dest_file)
            return dest_file
        except Exception:
            return None

    def fetchfilefrompath(self, i_startswith, i_endswith, i_path):
        """
            get file details
        """
        if not i_startswith or not i_endswith or not i_path:
            return None

        for s3_file in self.s3_bucket.objects.filter(Prefix=i_path):
            """
                check if filename match
            """
            file_name = os.path.basename(str(s3_file.key))
            if file_name.startswith(i_startswith) and \
                    file_name.endswith(i_endswith):
                """
                    file match's let's return
                """
                return self.fetchfilefromkey(s3_file.key)

        return None
