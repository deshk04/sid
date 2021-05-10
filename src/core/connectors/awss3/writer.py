"""
  Description:    file writer client
"""
import os
import logging

import csv
from core.connectors.file.writer import Writer as FileWriter
from core.general.exceptions import SIDException
from core.general.sidhelper import generate_filename, get_downloadpath


class Writer(FileWriter):
    """
        The class responsiblities are:
            Write csv file
    """

    def __init__(self, *args, **kwargs):
        self.s3client = None

        allowed_fields = set(['user_id', 'run_date', 'config'])
        for field in allowed_fields:
            try:
                setattr(self, field, kwargs[field])
            except Exception:
                setattr(self, field, None)
        super().__init__(*args, **kwargs)

    def setup(self, header):
        """
            we should open s3 connection
        """
        from core.connectors.awss3.client import AwsS3Client

        self.s3client = AwsS3Client()
        self.s3client.getclient(self.config.conn_object)
        self.s3client.connector = self.config.conn_object

        super().set_connLocal()
        return super().setup(header)

    def down(self):
        """
            clean up
        """
        super().down()
        """
            move the file to S3
        """
        self.s3client.s3_bucket.upload_file(
            super().file_name,
            self.config.file_path
        )
        """
            remove file
        """
        if os.path.isfile(super().file_name):
            os.remove(super().file_name)

    # def __del__(self):
    #     if self.fileptr:
    #         self.fileptr.close()
