import unittest
import os
import sys
import logging


class TestConnectors(unittest.TestCase):
    def test_fileconnector(self):
        """
            Test file connector
        """
        from core.general.appinit import setup_django
        setup_django()

        from core.connectors.file.writer import Writer
        from core.models.coreproxy import JobConfigProxy, ConnectorProxy
        from core.models.coreproxy import DimConnectorProxy
        from core.general import settings

        dim_connector = DimConnectorProxy(
            conn_name='File'
        )
        connector = ConnectorProxy(
            name='test',
            conn_name=dim_connector
        )
        config = JobConfigProxy(
            filepath=settings.DOCUMENT_PATH,
            filestartwith='unittest_file',
            fileendwith='.csv',
            conn_object=connector
        )
        config.filepath = config.filepath + 'admin'
        writer = Writer(
            user_id='admin',
            run_date=None,
            config=config
        )
        wheader = [{'field_name': 'field1'}, {'field_name': 'field2'}]
        writer.setup(wheader)
        wrecord = {'field1': 'abcd', 'field2': 'xyz'}
        writer.write(wrecord)
        writer.down()

        from core.connectors.file.reader import Reader
        reader = Reader(
            user_id='admin',
            run_date=None,
            config=config
        )
        reader.setup()
        rheadero = []
        for field in reader.header:
            rheadero.append({'field_name': field['field_name']})

        self.assertListEqual(wheader, rheadero)

        # rrecord = []
        # for rec in reader.read():
        #     rrecord.append(rec)
        rrecord = [rec for rec in reader.read()]

        reader.down()

        self.assertDictEqual(wrecord, rrecord[0])

        if os.path.isfile(reader.filename):
            os.remove(reader.filename)
