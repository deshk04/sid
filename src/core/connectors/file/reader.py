"""
  Description:    filereader client
"""

import os
import logging
import csv
from core.general.exceptions import SIDException
from core.general.sidhelper import generate_filename, convert_field


class Reader():
    """
        The class responsiblities are:
            Read csv file, header record etc
        if you want to use this class on its own then
        setup filename and call setup(), read()
    """
    def __init__(self, *args, **kwargs):
        self.filename = None
        self.fileptr = None
        self.reader = None
        self.filesize = 0
        self.header_fields = []
        self.encoding = 'utf-8-sig'
        self.delimiter = ','
        self.lineterminator = '\n'

        allowed_fields = set(['user_id', 'run_date', 'config'])
        for field in allowed_fields:
            try:
                setattr(self, field, kwargs[field])
            except Exception:
                setattr(self, field, None)

        if not self.config.encoding or self.config.encoding == 'utf-8':
            self.encoding = 'utf-8-sig'
        else:
            self.encoding = self.config.encoding

        if not self.config.delimiter:
            self.delimiter = ','
        else:
            self.delimiter = self.config.delimiter

        if not self.config.lineterminator or \
                self.config.lineterminator in ['LF', '\n']:
            self.lineterminator = '\n'
        else:
            self.lineterminator = '\r\n'

    def get_filename(self):
        """
            get the filename from config
        """
        if not self.config.filepath or not self.config.filestartwith:
            raise SIDException('Mandatory field is missing', 'filename')

        self.filename = generate_filename(
            self.config.filepath,
            self.config.filestartwith,
            self.config.fileendwith,
            self.run_date,
            self.config.filemask
        )

    def set_filename(self, filename):
        """
            set the filename
        """
        self.filename = filename

    def setup(self):
        """
            setup connection
        """
        self.get_filename()

        if not os.path.isfile(self.filename):
            return False

        self.open()

    def open(self):
        """
            open file
        """

        self.fileptr = open(
            self.filename,
            mode='r',
            encoding=self.encoding)

        self.reader = csv.DictReader(
            self.fileptr, quotechar='"',
            delimiter=self.delimiter,
            quoting=csv.QUOTE_ALL,
            skipinitialspace=True,
            lineterminator=self.lineterminator)

        if not self.reader:
            raise SIDException('error reading file', self.filename)

        size = os.path.getsize(self.filename)
        try:
            self.filesize = size / 1024 / 1024
        except Exception:
            logging.error('Error reading file size')

    @property
    def header(self):
        """
            return header
        """
        self.fetchheader()
        return self.header_fields

    @property
    def input_object(self):
        if self.filename:
            return os.path.basename(self.filename)
        return None

    def fetchmodel(self):
        """
            get model record
        """
        modellist = []
        """
            populate model record
            this is filename with datetime stamp
        """
        name = self.file_name
        record = {
            'name': name,
            'label': None,
            'readable': None,
            'writeable': None
        }

        modellist.append(record)
        return modellist

    def fetchheader(self):
        """
            get header record
        """
        if self.reader:
            for field in self.reader.fieldnames:
                """
                    populate header record
                    in future we will derive the datatype
                """
                self.header_fields.append(convert_field(field))
        return self.header_fields

    def read(self):
        """
            get file details
        """
        for record in self.reader:
            yield record

    def down(self):
        """
            clean up
        """
        if self.fileptr:
            self.fileptr.close()
