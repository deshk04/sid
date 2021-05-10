"""
  Description:    Response class
"""

import json
from datetime import datetime, date


class ApiResponse():
    """
        we need to output an standard json such that angular
        always know what to expect
        below is the format
        {
            status:
            message:
            num_of_records:
            records: list of records
        }
    """

    def __init__(self, *args, **kwargs):
        self.status = 'ok'
        self.message = []
        self.num_of_records = 0
        self.records = None

    def setrecords(self, result):
        """
            set records
        """
        self.records = result

    def updatecount(self):
        if self.records is not None:
            self.num_of_records = len(self.records)
        else:
            self.num_of_records = 0
            self.records = {}

    def dumpoutput(self):
        """
            output records
        """
        if not self.num_of_records or self.num_of_records == 0:
            self.updatecount()
        return json.dumps(self.__dict__, default=self.datetime_handler)

    def getdict(self):
        """
            output dict
        """
        self.updatecount()
        return self.__dict__

    def datetime_handler(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)

    def __str__(self):
        """
            print all the variables
        """
        return str(self.__class__) + ": " + str(self.__dict__)
