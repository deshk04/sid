"""
  Description:    aws3 reader
"""

import os
import logging
import uuid

from core.general.exceptions import SIDException
from core.general.sidhelper import generate_filename, get_downloadpath
from core.connectors.file.reader import Reader as FileReader

class Reader(FileReader):
    """
        The class responsiblities are:
            download the file from s3 and let FileReader do the rest
    """
    def __init__(self, *args, **kwargs):
        self.fileptr = None
        self.reader = None
        self.filesize = 0
        self.header_fields = []
        self.s3client = None

        allowed_fields = set(['user_id', 'run_date', 'config'])
        for field in allowed_fields:
            try:
                setattr(self, field, kwargs[field])
            except Exception:
                setattr(self, field, None)
        super().__init__(*args, **kwargs)

    def setup(self):
        """
            setup connection
        """
        from core.connectors.awss3.client import AwsS3Client

        self.s3client = AwsS3Client()
        self.s3client.getclient(self.config.conn_object)
        self.s3client.connector = self.config.conn_object
        filename = generate_filename(
            filepath=None,
            filestartwith=self.config.filestartwith,
            fileendwith=None,
            run_date=self.run_date,
            filemask=self.config.filemask
        )
        local_dir = get_downloadpath(self.user_id)
        try:
            self.filename = self.download(
                self.config.filepath,
                filename,
                self.config.fileendwith,
                local_dir
            )
        except Exception:
            logging.debug('Error in awss3controller download')
            self.filename = None

        """
            If no input file exists then return
        """
        if not self.filename or not os.path.isfile(self.filename):
            return False

        super().set_filename(self.filename)
        super().open()

    def download(self, filepath, filestartwith, fileendwith, local_dir):
        """
            download the file
        """
        logging.debug('awss3controller: download')
        if not self.s3client:
            return None

        logging.debug('searching in...')
        logging.debug(filepath)
        fileobjects = []
        try:
            for obj in self.s3client.s3_bucket.objects.filter(Prefix=filepath):
                rfilename = os.path.basename(obj.key)
                """
                    check if the file exists
                """
                if rfilename.startswith(filestartwith) and rfilename.endswith(fileendwith):
                    fileobjects.append(obj.key)
        except Exception:
            raise SIDException('Exception in s3client')

        if len(fileobjects) < 1:
            logging.debug('awss3controller: file not found')
            return None

        logging.debug('awss3controller: file found')
        logging.debug(fileobjects)
        fileobjects.sort()
        newfile = fileobjects[-1]
        targetfilename = os.path.basename(newfile)
        """
            we should make filename unique
        """
        uniqstring = str(uuid.uuid4())[:8]
        try:
            filepart = os.path.splitext(targetfilename)
            newtarget = filepart[0] + '_' + uniqstring + filepart[1]
            targetfilename = newtarget
        except Exception:
            targetfilename = targetfilename + '_' + uniqstring

        target = local_dir + os.path.basename(targetfilename)
        logging.debug('newfile: ')
        logging.debug(target)
        """
            remove old file
        """
        if os.path.isfile(target):
            os.remove(target)

        logging.debug('awss3controller: downloading file')
        self.s3client.s3_bucket.download_file(newfile, target)

        return target

    def down(self):
        """
            clean up
        """
        if self.filename:
            if os.path.isfile(self.filename):
                os.remove(self.filename)

    def __del__(self):
        if self.filename:
            if os.path.isfile(self.filename):
                os.remove(self.filename)
