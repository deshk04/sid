"""
  Description:    file writer client
"""

import logging

import csv
from core.general.exceptions import SIDException
from core.general.sidhelper import generate_filename, get_downloadpath


class Writer():
    """
        The class responsiblities are:
            Write csv file    """

    def __init__(self, *args, **kwargs):
        self.fileptr = None
        self.reader = None
        self.filesize = 0
        self.filetype = 'text'

        allowed_fields = set(['user_id', 'run_date', 'config'])
        for field in allowed_fields:
            try:
                setattr(self, field, kwargs[field])
            except Exception:
                setattr(self, field, None)

        if not self.config.encoding or self.config.encoding == 'utf-8':
            self.config.encoding = 'utf-8-sig'
        if not self.config.delimiter:
            self.config.delimiter = ','
        if not self.config.lineterminator or self.config.lineterminator == 'LF':
            self.config.lineterminator = '\n'
        else:
            self.config.lineterminator = '\r\n'

    def set_connLocal(self):
        """
            set connector as local
        """
        self.config.conn_object.conn_name.conn_name = 'File'

    def setup(self, header):
        """
            open file
        """
        """
            if config is sidLocal then we should generate filename
        """
        if self.config.conn_object.conn_name.conn_name.lower() == 'file':
            self.file_path = get_downloadpath(self.user_id)
            self.file_name = generate_filename(
                filepath=self.file_path,
                filestartwith=self.config.filestartwith,
                fileendwith=self.config.fileendwith,
                run_date=self.run_date,
                filemask=self.config.filemask
            )

        if not self.file_path or not self.file_name:
            raise SIDException('Mandatory field is missing', 'filename')

        self.fileptr = open(self.file_name, mode='w', encoding=self.config.encoding)

        if self.filetype != 'json':
            if not header:
                raise SIDException('error writing file: header missing', self.file_name)
            self.writer = csv.DictWriter(
                self.fileptr, quotechar='"',
                delimiter=self.config.delimiter,
                quoting=csv.QUOTE_ALL,
                fieldnames=[field['field_name'] for field in header],
                lineterminator=self.config.lineterminator)

            if not self.writer:
                raise SIDException('error writing file', self.file_name)
            self.writer.writeheader()

    def write(self, map_record, orig_record=None):
        """
            get file details
        """

        if self.filetype == 'json':
            self.fileptr.write(map_record)
        else:
            self.writer.writerow(map_record)

    @property
    def output_object(self):
        return []

    def down(self):
        """
            clean up
        """
        if self.fileptr:
            self.fileptr.close()

    # def __del__(self):
    #     if self.fileptr:
    #         self.fileptr.close()
