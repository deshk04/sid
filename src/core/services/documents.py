"""
  Description:    Document service
"""

import os
import csv
# import boto3
from core.general import settings


class DocumentsService():
    """
        The class responsiblities are:
            find the fields
    """

    def __init__(self, *args, **kwargs):
        self.localfile = None
        self.filename = None
        self.delimiter = None
        self.lineterminator = None
        self.user_id = None
        self.fields = []
        self.filepath = ''

    def findfields(self):
        try:
            lineterminator = self.getlineterminator()

            with open(self.localfile, mode='r', encoding='utf-8-sig') as fileptr:
                reader = csv.reader(
                    fileptr, quotechar='"',
                    delimiter=self.delimiter,
                    quoting=csv.QUOTE_ALL,
                    skipinitialspace=True,
                    lineterminator=lineterminator)
                for record in reader:
                    """
                        assuming we have a header record
                    """
                    for field in record:
                        output = {}
                        output['field_name'] = field
                        output['field_type'] = 'Auto'
                        output['field_length'] = None
                        output['field_format'] = None
                        output['label'] = None
                        output['primary_key'] = None
                        self.fields.append(output)
                    break
        except Exception:
            self.remove_file(self.localfile)
            return None

        self.remove_file(self.localfile)
        return self.fields

    def getlineterminator(self):
        """
            convert line number
        """
        lineterminator = '\n'
        if self.lineterminator and self.lineterminator == 'CRLF':
            self.lineterminator = '\r\n'

        return lineterminator

    def process_document(self, inputfile, getfields='Y'):
        """
            get all file details
        """
        if not inputfile:
            return None

        from django.core.files.storage import FileSystemStorage

        filepath = self.get_downloadpath()
        self.filename = inputfile.name.strip()
        self.localfile = filepath + self.filename

        """
            check if the file already exists at this location.
            if it does, delete it
        """
        self.remove_file(self.localfile)

        try:
            fs = FileSystemStorage(location=filepath)
            fs.save(self.localfile, inputfile)
            # self.localfile = filepath + self.filename
            if getfields == 'Y':
                record = self.findfields()
                return record
            else:
                return self.localfile
        except Exception:
            return None

    def process_s3document(self, inputfile):
        """
            get all file details
        """
        if not inputfile:
            return None
        self.localfile = inputfile

        try:
            record = self.findfields()
            return record
        except Exception:
            return None

    def remove_file(self, filename):
        if os.path.exists(filename):
            os.unlink(filename)

    def set_filename(self, filename):
        self.filename = os.path.basename(filename)
        self.filepath = os.path.dirname(filename)

    def get_docodetails(self):
        file_name, file_ext = os.path.splitext(self.filename)
        config = {
            'filepath': self.filepath,
            'filestartwith': file_name,
            'fileendwith': file_ext,
            'filemask': '',
            'delimiter': self.delimiter,
            'encoding': 'utf-8',
            'lineterminator': self.lineterminator
        }
        return config

    def get_downloadpath(self):
        """
            find the download path
        """
        if not self.user_id:
            self.user_id = settings.SID_ADMIN

        path = settings.DOCUMENT_PATH + str(self.user_id) + '/temp/'
        if not os.path.isdir(path):
            os.mkdir(path)

        return path
