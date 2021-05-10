"""
  Description:    Salesforce Writer
"""
import logging

from simple_salesforce.exceptions import SalesforceExpiredSession
from simple_salesforce.exceptions import SalesforceGeneralError
from simple_salesforce.exceptions import SalesforceMalformedRequest
from simple_salesforce.exceptions import SalesforceRefusedRequest
from simple_salesforce.exceptions import SalesforceResourceNotFound
from simple_salesforce.exceptions import SalesforceError

from django.utils import timezone

from core.general.exceptions import SIDException
from core.general import settings


class Writer:
    """
        Salesforce Writer
    """

    def __init__(self, *args, **kwargs):
        self.sfclient = None
        self.bulk_count = 1
        self.primary_key = None
        self.dest_model = None
        self.transaction_type = None
        self.orig_records = []
        self.data_records = []
        self.reponse_details = []

        allowed_fields = set(['user_id', 'run_date', 'config'])
        for field in allowed_fields:
            try:
                setattr(self, field, kwargs[field])
            except Exception:
                setattr(self, field, None)

    def setup(self, header):
        """
            setup connection
        """
        logging.debug("SFController: setup")

        from core.connectors.salesforce.client import SalesforceClient
        sfclient = SalesforceClient()
        self.sfclient = sfclient.getclient(self.config.conn_object)
        self.dest_model = self.config.model

        return self.set_writer()

    def set_writer(self):
        """
            set up bulk properties
        """
        self.set_bulkcount(self.config.bulk_count)
        self.set_pkey(self.config.key_field)
        self.set_transactiontype(self.config.transaction_type)

    def set_bulkcount(self, bulk_count):
        """
            set bulk count
        """
        self.bulk_count = bulk_count
        if not self.bulk_count:
            from core.services.sidsettings import SidSettingsService
            sid_settings = SidSettingsService(
                user_id=self.user_id
            )
            self.bulk_count = sid_settings.getkeyvalue_as_num('BULK_COUNT')
            if self.bulk_count:
                self.bulk_count = settings.BULK_COUNT

    def set_pkey(self, primary_key):
        """
            set primary key
        """
        self.primary_key = primary_key

    def set_transactiontype(self, transaction_type):
        """
            set transaction type
        """
        if transaction_type:
            self.transaction_type = self.transaction_type
            if self.transaction_type not in ["insert", "update", "upsert"]:
                self.transaction_type = None

    def write(self, map_record, orig_record):
        """
            write record

            orig_record: record before transformation was applied,
            orig_record is only used to log an error with orig_record such
            that it can be reprocessed easily

            map_record: record after transformation was applied
            map_record is sent to salesfore
        """
        self.orig_records.append(orig_record)
        self.data_records.append(map_record)
        if len(self.data_records) >= self.bulk_count:
            responserecs = self.bulk_write()
            self.set_response(responserecs)
            """
                we set up response records
            """
            self.data_records = []
            self.orig_records = []

    def bulk_write(self):
        """
            process the records
        """
        logging.debug('Inside bulk write')
        result = None
        try:
            if self.primary_key:
                """
                    do a bulk update
                """
                result = self.sfclient.bulk.__getattr__(self.dest_model).upsert(
                    self.data_records,
                    self.primary_key,
                    batch_size=len(self.data_records),
                    use_serial=True,
                )
            elif self.transaction_type and self.transaction_type == "update":
                result = self.sfclient.bulk.__getattr__(
                    self.dest_model).update(
                        self.data_records,
                        batch_size=len(self.data_records),
                        use_serial=True,
                )
            else:
                result = self.sfclient.bulk.__getattr__(
                    self.dest_model).insert(
                    self.data_records,
                    batch_size=len(self.data_records),
                    use_serial=True,
                )
        except SalesforceExpiredSession as sexp:
            raise SIDException(str(sexp))
        except SalesforceMalformedRequest as sexp:
            raise SIDException(str(sexp))
        except SalesforceRefusedRequest as sexp:
            raise SIDException(str(sexp))
        except SalesforceResourceNotFound as sexp:
            raise SIDException(str(sexp))
        except SalesforceError as sexp:
            raise SIDException(str(sexp))
        except SalesforceGeneralError as sexp:
            """
                we should rerun the query?
            """
            raise SIDException(str(sexp))
        except Exception as ex:
            logging.error("Error processing records")
            raise SIDException("Error processing records: ", str(ex.errors))

        return result

    def set_response(self, responserecs):
        """
            set response in JobRunDetails format
        """
        if responserecs:
            """
                parse the result response
            """

            error_reccount = 0
            for record in responserecs:
                response = self.parse_response(record)
                if response["status"] == "failure":
                    job_details = {
                        'sys_creation_date': timezone.now(),
                        'record_key': response["field_key"],
                        'record_value': response["field_value"],
                        'status_code': response["status"],
                        'status_message': response["message"],
                        'processed_record': self.data_records[error_reccount],
                        'orig_record': self.orig_records[error_reccount]
                    }
                    """
                        assuming the response is in same order as
                        input we can track which record is the problem
                    """
                    self.reponse_details.append(job_details)
                error_reccount += 1

    @property
    def output_object(self):
        return self.reponse_details

    def parse_response(self, record):
        """
            parse SF response
        """
        response = {
            "status": "failure",
            "field_key": "id",
            "field_value": None,
            "message": None,
        }
        if record:
            try:
                if record.get("success", None):
                    response["status"] = "success"
                if record.get("id", None):
                    response["field_value"] = record["id"]
                if record.get("errors", None):
                    message = ""
                    for item in record["errors"]:
                        message += str(item)
                    response["message"] = message
            except Exception:
                logging.error("Error decoding response")
                return response

        return response

    def down(self):
        """
            close any open connection
            and process unprocessed records
        """
        if self.data_records:
            responserecs = self.bulk_write()
            self.set_response(responserecs)
            """
                we set up response records
            """
            self.data_records = []
            self.orig_records = []
