# Connectors

SID Connectors area

## Setup

Every Connector is required minimum 2 files

* reader.py
* writer.py

additional files for some connectors can be

* client.py
    * client should be created if the connector requires to setup connection for e.g. salesforce, aws s3 etc
* mapper.py
    * mapper should be created if the writer has to do mapping

## Skeleton for reader.py

Each reader should implement below methods

```reader.py

import logging
from core.general.exceptions import SIDException

class Reader():
    """
        Connector reader
    """
    def __init__(self, *args, **kwargs):
        allowed_fields = set(['user_id', 'run_date', 'config'])
        for field in allowed_fields:
            try:
                setattr(self, field, kwargs[field])
            except Exception:
                setattr(self, field, None)

    def setup(self):
        """
            setup connection
        """
        pass

    @property
    def header(self):
        """
            return header
        """
        pass

    def read(self):
        """
            read record
        """
        pass

    def down(self):
        """
            close reader
        """
        pass

```

## Skeleton for writer.py

Each writer should implement below methods

```writer.py

import logging
from core.general.exceptions import SIDException

class Writer():
    """
        Connector reader
    """
    def __init__(self, *args, **kwargs):
        allowed_fields = set(['user_id', 'run_date', 'config'])
        for field in allowed_fields:
            try:
                setattr(self, field, kwargs[field])
            except Exception:
                setattr(self, field, None)

    def setup(self, destination_object):
        """
            setup connection
            destination_object: tablename / objectname where data will be
            written
        """
        pass


    def write(self):
        """
            read record
        """
        pass

    def down(self):
        """
            close writer
        """
        pass

```

## Skeleton for mapper.py

Each mapper should implement below methods

```mapper.py

import logging
from core.general.exceptions import SIDException

class Mapper():
    """
        Connector mapper
    """
    def __init__(self, *args, **kwargs):
        allowed_fields = set(['user_id', 'run_date', 'config'])
        for field in allowed_fields:
            try:
                setattr(self, field, kwargs[field])
            except Exception:
                setattr(self, field, None)

    def setup(self):
        """
            setup connection
        """
        pass


    def write(self):
        """
            read record
        """
        pass

    @property
    def destination_object(self):
        """
            return destination object
        """
        pass

    def down(self):
        """
            close writer
        """
        pass

```
