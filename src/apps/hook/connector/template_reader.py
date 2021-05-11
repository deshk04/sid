"""
  Description:    template reader
"""

import os
import logging
import csv
from core.general.exceptions import SIDException
from core.general.sidhelper import generate_filename, convert_field


class Reader():
    """
        Template Reader based on
        core.connector.file.reader
    """
    def __init__(self, *args, **kwargs):
        self.reader = None
        self.header_fields = ['run_date']

        allowed_fields = set(['user_id', 'run_date', 'config'])
        for field in allowed_fields:
            try:
                setattr(self, field, kwargs[field])
            except Exception:
                setattr(self, field, None)

    def setup(self):
        """
            setup connection to external connector
        """
        self.open()

    def open(self):
        """
            open connection
            in template we populate dummy data
        """
        self.reader = [{'run_date__c': self.run_date.strftime('%Y-%m-%d')}]

    @property
    def header(self):
        """
            return header
        """
        return self.header_fields

    @property
    def input_object(self):
        return 'dummy'

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
        pass
