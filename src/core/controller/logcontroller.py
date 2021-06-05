"""
  Description:    Log Controller
"""
import os
import logging
import time
import xlsxwriter
import csv

from core.general import settings


class LogController():
    """
        Log Controller
    """

    def __init__(self, *args, **kwargs):
        self.job = None
        self.jobrun = None
        self.jobrundetails = None
        self.log_file = None

        allowed_fields = set(['user_id'])
        for field in allowed_fields:
            try:
                setattr(self, field, kwargs[field].strip())
            except Exception:
                setattr(self, field, None)

    def execute(self, rtype='all'):
        """
            run the job
        """
        if not self.jobrun or not self.job:
            """
                make sure user is populated
                we dont generate error in logcontroller
            """
            return None

        logging.debug('LogController: execute')
        """
            produce the output
        """
        from core.models.coreproxy import JobrunDetailsProxy
        self.jobrun_details = JobrunDetailsProxy.objects.filter(
            jobrun_id=self.jobrun.id
        )
        if self.jobrun_details:
            """
                produce the file
            """
            if rtype == 'error':
                self.csv_file()
            else:
                self.excel_file()

    def excel_file(self):
        """
            produce excel output
        """
        workbook = None
        worksheet = None
        """
            we found some records to let's create the header for output
        """
        path = settings.LOGFILE_PATH + str(self.user_id) + '/'
        if not os.path.isdir(path):
            os.mkdir(path)

        log_file = self.job.job_name + '_' + \
            self.jobrun.run_date.strftime('%Y%m%d') + \
            '_' + str(self.jobrun.id) + '.xlsx'
        self.log_file = path + log_file
        """
            if file exists remove it
        """
        if os.path.isfile(self.log_file):
            os.remove(self.log_file)

        """
            let's create worksheet
        """
        workbook = xlsxwriter.Workbook(self.log_file)
        worksheet = workbook.add_worksheet()
        header_format = workbook.add_format({
            'border': 1,
            'bg_color': '#C6EFCE',
            'bold': True,
            'text_wrap': True,
            'valign': 'vcenter',
            'indent': 1,
            'locked': False,
        })

        unlocked = workbook.add_format({'locked': False})
        # locked = workbook.add_format({'locked': True})

        worksheet.write('A1', 'key', header_format)
        worksheet.write('B1', 'value', header_format)
        worksheet.write('C1', 'code', header_format)
        worksheet.write('D1', 'message', header_format)
        worksheet.write('E1', 'record', header_format)

        sheet_row = 1
        sheet_col = 0
        for jobdetail in self.jobrun_details:
            i = 0
            self.custome_write(worksheet,
                               sheet_row,
                               sheet_col + i,
                               str(jobdetail.record_key), unlocked)
            self.custome_write(worksheet,
                               sheet_row,
                               sheet_col + i + 1,
                               str(jobdetail.record_value), unlocked)
            self.custome_write(worksheet,
                               sheet_row,
                               sheet_col + i + 2,
                               str(jobdetail.status_code),
                               unlocked)
            self.custome_write(worksheet,
                               sheet_row,
                               sheet_col + i + 3,
                               str(jobdetail.status_message),
                               unlocked)
            self.custome_write(worksheet,
                               sheet_row,
                               sheet_col + i + 4,
                               str(jobdetail.orig_record),
                               unlocked)

            sheet_row += 1

        if worksheet:
            workbook.close()
            """
                lets put delay to make sure file is written correctly
            """
            time.sleep(6)

        return self.log_file

    def csv_file(self):
        """
            produce csv output
        """

        """
            we found some records to let's create the header for output
        """
        path = settings.LOGFILE_PATH + str(self.user_id) + '/'
        if not os.path.isdir(path):
            os.mkdir(path)

        log_file = self.job.job_name + '_' + \
            self.jobrun.run_date.strftime('%Y%m%d') + \
            '_' + str(self.jobrun.id) + '.csv'
        self.log_file = path + log_file
        """
            if file exists remove it
        """
        if os.path.isfile(self.log_file):
            os.remove(self.log_file)

        """
            let's write csv
        """
        import ast
        fields, records = [], []
        # p = re.compile('(?<!\\\\)\'')
        reccount = 0
        curr_record = None

        if self.jobrun_details:
            for jobdetail in self.jobrun_details:
                if jobdetail.status_code == 'failure':
                    if jobdetail.orig_record:
                        try:
                            record = []
                            curr_record = jobdetail.orig_record
                            curr_record = ast.literal_eval(
                                jobdetail.orig_record)
                            # jstr = jstr[1:]
                            # jstr = jstr[:-1]
                            # jstr = p.sub('\"', jstr)
                            # jstr = jobdetail.orig_record.replace("\'","\"")
                            # jstr = jstr.replace(': None,', ': "",')
                            # jstr = jstr.replace(': None}', ': ""')
                            # dictrec = dict(json.loads(jstr))
                            for key, value in curr_record.items():
                                record.append(value)

                            records.append(record)
                            reccount += 1
                        except Exception as exp:
                            logging.error('Error in converstion')

        if reccount > 0:
            for key, value in curr_record.items():
                fields.append(key)

        with open(self.log_file, 'w') as errorfile:
            writer = csv.writer(errorfile, delimiter='|')

            writer.writerow(fields)
            for rec in records:
                writer.writerow(rec)

        return self.log_file

    def custome_write(self, worksheet, sheet_row, sheet_col, field, lock):
        """
            check if the field is None or not
        """
        if field is None:
            worksheet.write_blank(sheet_row, sheet_col, None, lock)
        else:
            worksheet.write_string(sheet_row, sheet_col, str(field), lock)

    def get_summary(self):
        """
            generate summary
        """
        summary = """
                    <html>
                    <head>Job: {0}</head>
                    <body>
                        <p>Total Number of records: {1} <br></p>
                        <p>Number of records Successfull: {2} <br></p>
                        <p>Number of records Failed: {3} <br></p>
                    </body>
                    </html>
                    """
        summary = summary.format(
            self.job.job_name,
            str(self.jobrun.total_count),
            str(self.jobrun.success_count),
            str(self.jobrun.failure_count)
        )

        return summary

    def get_title(self):
        """
            get title
        """
        title = "Job: {0} for rundate: {1}".format(
            self.job.job_name,
            str(self.jobrun.run_date)
        )
        return title
