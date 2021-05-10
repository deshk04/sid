"""
  Description:    Schedule Mapper
"""
from datetime import datetime, date, timedelta
import logging
from concurrent import futures

from django.utils import timezone
from django.db.models import Q
from django.db.models import Max

from core.general import settings
from core.general.exceptions import SIDException


class ScheduleController():
    """
        Schedule Controller
    """

    def __init__(self, *args, **kwargs):
        self.schedule_id = None
        self.schedule = None
        self.schedule_config = None
        self.schedule_log = None
        self.run_date = None
        self.mark_complete = False

        allowed_fields = set(['user_id', 'schedule_id'])
        for field in allowed_fields:
            try:
                setattr(self, field, kwargs[field])
            except Exception:
                setattr(self, field, None)

    def execute(self, rerun_flag='N'):
        """
            run the
        """
        logging.debug('Schedule Started')

        if not self.user_id or not self.schedule_id:
            """
                make sure user / schedule_name is populated
            """
            raise SIDException('Mandatory Field Missing', 'User / name')

        logging.debug('Starting Schedule: %s', str(self.schedule_id))

        from core.services.sidsettings import SidSettingsService
        sid_settings = SidSettingsService(
            user_id=self.user_id
        )
        if not sid_settings.settings:
            """
                user settings missing
            """
            raise SIDException('User settings missing')

        from core.models.coreproxy import ScheduleProxy, ScheduleLogProxy
        """
            check if the Schedule is active
        """
        """
            If admin is running the schedule
            then dont check owner
        """
        query = Q(Q(
            schedule__object_type='Schedule') & Q(
                schedule_id=self.schedule_id) & Q(
                Q(schedule__expiration_date__gte=datetime.today()
                  ) | Q(schedule__expiration_date__isnull=True)
        )
        )
        if sid_settings.sidadmin != self.user_id:
            query = Q(
                Q(schedule__object_type='Schedule') & (
                    Q(schedule__object_owner=self.user_id) | Q(
                        schedule__object_owner=settings.SID_ADMIN)) & Q(
                            schedule_id=self.schedule_id) & Q(
                    Q(schedule__expiration_date__gte=datetime.today()) | Q(
                        schedule__expiration_date__isnull=True)
                )
            )

        schedule_records = ScheduleProxy.objects.filter(
            query
        )

        if len(schedule_records) < 1:
            """
                job is not active
            """
            raise SIDException('No Active Schedule found', self.schedule_name)

        self.schedule = schedule_records[0]

        """
            let's find the run date
            -- for the time we assume all our schedule are daily
        """
        logging.debug('Source and Destination configuration fetched')
        """
            if rerun flag is set then we dont check if the job
            is already run
        """
        if self.mark_complete:
            if not self.run_date:
                """
                    if schedule is to be marked as complete
                    then rundate should be populated
                """
                raise SIDException('Invalid Run Date for mark to complete', '')

        elif rerun_flag == 'Y':
            if not self.run_date:
                """
                    we check if self.run_date is populated or not
                """
                raise SIDException('Invalid Run Date for Rerun', '')

        elif rerun_flag == 'N':
            """
                fetch the run date
            """

            if not self.schedule.frequency:
                raise SIDException('Invalid Job Frequency', '')

            new_jobdate = None
            new_jobdate = self.get_rundate()

            if not new_jobdate:
                logging.debug('Job not running for this date')
                return

            """
                process the job
            """
            logging.debug('Processing schedule for: %s', str(new_jobdate))

            """
                we check if the schedule is running
            """
            schedulerrunning = ScheduleLogProxy.objects.get_or_none(
                schedule_id=self.schedule.schedule_id,
                status='Running',
                run_date=new_jobdate
            )
            if not schedulerrunning:
                """
                    now we have data for the day run so
                    let's produce the output
                """
                self.run_date = new_jobdate
            else:
                logging.debug('Job is running')
                return

        self.run_schedule(rerun_flag)
        logging.debug('Schedule Finished')

        return True

    def get_rundate(self):
        """
            based on schedule frequency get the run date
        """
        new_jobdate = None
        frequency = self.schedule.frequency.lower()
        if frequency not in ['daily', 'monthly']:
            raise SIDException('Invalid frequency')

        """
            when a new job is created, front end should
            create a dummy complete record so
            we always expect atleast 1 record for each
            schedule
        """
        from core.models.coreproxy import ScheduleLogProxy
        schedulerrun = ScheduleLogProxy.objects.filter(
            schedule_id=self.schedule.schedule_id,
            status='Complete'
        ).aggregate(Max('run_date'))

        if not self.schedule.day_of_week:
            self.schedule.day_of_week = '0,1,2,3,4,5,6'

        """
            we check the days for which the schedule should run
        """
        if frequency == 'daily':
            """
                we add 1 to last complete date and run
                the schedule for this run date
            """
            last_jobdate = schedulerrun['run_date__max']
            new_jobdate = last_jobdate + timedelta(days=+1)
            days_to_run = self.schedule.day_of_week.split(',')
            if str(new_jobdate.weekday()) not in days_to_run:
                """
                    skip the day, mark it as complete
                """
                schedulerrunning = ScheduleLogProxy(
                    sys_creation_date=timezone.now(),
                    user_id=self.user_id,
                    schedule=self.schedule,
                    run_date=new_jobdate,
                    status='Complete',
                    message='Day to Skip: no run'
                )
                schedulerrunning.save()
                logging.debug('Schedule Finished')
                return None
            return new_jobdate
        elif frequency == 'monthly':
            """
                we dont check the last jobrun
            """
            try:
                day_of_month = int(self.schedule.day_of_month)
            except Exception as exp:
                raise SIDException('Schedule: Invalid day of month')

            jobdate = date.today()
            if jobdate.day == day_of_month:
                return jobdate
            """
                if day of month is 0 then we run it for last
                of month
            """
            njobdate = jobdate + timedelta(days=+1)
            if njobdate.day == 1 and self.schedule.day_of_month:
                return jobdate

            """
                we skip the day
            """

        return None

    def run_schedule(self, rerun_flag):
        """
            run the schedule
        """
        logging.debug('run_schedule')
        from core.services.sidsettings import SidSettingsService
        sid_settings = SidSettingsService(
            user_id=self.user_id
        )

        from core.models.coreproxy import ScheduleConfigProxy, ScheduleLogProxy
        schedule_steps = ScheduleConfigProxy.objects.filter(
            schedule_id=self.schedule.schedule_id,
            active_flag='Y'
        ).aggregate(Max('job_sequence'))
        if not schedule_steps:
            raise SIDException('Schedule config missing')

        self.schedule_log = ScheduleLogProxy(
            sys_creation_date=timezone.now(),
            user_id=self.user_id,
            schedule=self.schedule,
            run_date=self.run_date,
            status='Running'
        )
        self.schedule_log.message = ''
        self.schedule_log.save()
        max_stepno = schedule_steps['job_sequence__max']
        # for stepno in range(max_stepno, 0, -1):

        status = None
        jobrun_records = []
        for stepno in range(1, max_stepno + 1):
            schedule_steps = ScheduleConfigProxy.objects.filter(
                schedule_id=self.schedule.schedule_id,
                active_flag='Y',
                job_sequence=stepno
            ).values('job_id')
            if not schedule_steps:
                continue

            try:

                """
                    run all the jobs on this step in parallel
                """
                success = True
                schparallel = False
                if sid_settings.getkeyvalue('SCHEDULE_PARALLEL') == 'Y':
                    schparallel = True

                if schparallel:
                    logging.debug('Running schedule in parallel')
                    with futures.ProcessPoolExecutor(
                            max_workers=len(schedule_steps) + 1) as executor:
                        job_status = [executor.submit(
                            run_job,
                            jrun['job_id'],
                            self.run_date,
                            self.user_id,
                            rerun_flag,
                            self.schedule.schedule_id,
                            self.schedule_log.id,
                            self.mark_complete
                        ) for jrun in schedule_steps]
                    for rjob_id in futures.as_completed(job_status):
                        """
                            we check the status of the jobs
                            if there is failure then we terminate the job
                        """
                        status = rjob_id.result()
                        if status[1] != 1:
                            success = False
                            break

                else:
                    """
                        jobs are not run in parellel in this condition
                    """
                    logging.debug('Running schedule in sequence')
                    for jrun in schedule_steps:
                        status = run_job(
                            jrun['job_id'],
                            self.run_date,
                            self.user_id,
                            rerun_flag,
                            self.schedule.schedule_id,
                            self.schedule_log.id,
                            self.mark_complete
                        )
                        jobrun_records.append(status)
                        if status[1] != 1:
                            success = False
                            break

                if not success:
                    break

            except SIDException as exp:
                logging.debug('Job failure for %s', str(jrun['job_id']))
                error = str(exp)
                logging.debug(error)
                self.schedule_log.status = 'Failed'
                self.schedule_log.sys_update_date = timezone.now()
                self.schedule_log.message = 'Job failed: with exception' + \
                    str(error)
                self.schedule_log.save()
                success = False
                break

            except Exception as exp:
                self.schedule_log.status = 'Failed'
                self.schedule_log.sys_update_date = timezone.now()
                self.schedule_log.message = 'Job failed: with exception: ' + \
                    str(exp)
                self.schedule_log.save()
                success = False
                break

        if success:
            self.schedule_log.status = 'Complete'
            self.schedule_log.sys_update_date = timezone.now()
            self.schedule_log.message = 'all good'
            if self.mark_complete:
                self.schedule_log.message = 'marked as complete'
        else:
            if status:
                job_name = str(status[0])
                jobrun_rec = status[2]
                if jobrun_rec:
                    job_name = str(jobrun_rec.job_name)
                if status[1] == 0:
                    logging.debug('Job failure')
                    self.schedule_log.status = 'Failed'
                    self.schedule_log.message += ' \n Job failed: ' + job_name
                elif status[1] == 2:
                    logging.debug('Job Not ready')
                    self.schedule_log.status = 'Not Ready'
                    self.schedule_log.sys_update_date = timezone.now()
                    self.schedule_log.message = 'Job Not Ready - ' + job_name
            else:
                logging.debug('Job failure: no status')
                self.schedule_log.status = 'Failed'

        self.schedule_log.sys_update_date = timezone.now()
        self.schedule_log.save()

        schemail = False
        if sid_settings.getkeyvalue('SCHEDULE_EMAIL') == 'Y':
            schemail = True

        if schemail:
            from core.models.coreproxy import ScheduleDistributionProxy

            distribution = ScheduleDistributionProxy.objects.get_or_none(
                schedule_id=self.schedule.schedule_id
            )
            if not distribution:
                return

            subject = self.schedule.schedule_name + " : for " + \
                self.run_date.strftime("%Y-%m-%d")
            message = ""

            if success:
                """
                    we should send the message as success
                """
                message = """
                            <html>
                            <head>Schedule Run Details
                            <style>
                                table {
                                border-collapse: collapse;
                                width: 100%;

                                }

                                th, td {
                                text-align: left;
                                padding: 8px;
                                }
                                table, td, th {
                                border: 1px solid black;
                                }
                                tr:nth-child(even) {background-color: #f2f2f2;}

                                </style>
                            </head>
                            <body>
                                <p>Summary: <br>
                        """
                table = produce_html_table(jobrun_records)
                message += table
                message += """
                            </body>
                            </html>
                            """
            else:
                """
                    we send the message as failure
                """
                if status[1] == 2:
                    """
                        job not ready
                    """
                    message = """
                        <html>
                        <body>
                            Schedule Input not available
                        </body>
                        </html>
                        """

                else:
                    """
                        failure
                    """
                    message = """
                        <html>
                        <body>
                            Schedule failed: <br>
                            {0}
                        </body>
                        </html>
                        """.format(
                        self.schedule_log.message
                    )
            from core.clients.email import SIDEmail
            try:
                with SIDEmail() as sidemail:
                    sidemail.to_list = distribution.tolist
                    sidemail.cc_list = distribution.cclist
                    sidemail.send(
                        subject,
                        message
                    )
            except Exception:
                logging.error('Error sending email')

        return


def produce_html_table(records):
    """
        convert the list to table
    """
    code = """<table border='1'>
            <tr>
            <th>Job ID</th>
            <th>Status</th>
            <th>Job Name</th>
            <th>Total</th>
            <th>Success</th>
            <th>Fail</th>

            </tr>
          """
    for record in records:
        code += '  <tr><td>' + str(record[0])
        status = 'Success'
        if record[1] == 0:
            status = 'Failed'
        elif record[1] == 2:
            status = 'Not Ready'
        code += '    </td><td>' + status
        if record[2]:
            code += '    </td><td>' + str(record[2].job_name)
        else:
            code += '    </td><td>'
        if record[3]:
            total = str(record[3].total_count)
            success = str(record[3].success_count)
            failure = str(record[3].failure_count)
            code += '    </td><td>' + total
            code += '    </td><td>' + success
            code += '    </td><td>' + failure
        else:
            code += '    </td><td>'
            code += '    </td><td>'
            code += '    </td><td>'

        code += '  </td></tr>'
    code += '</table>'
    return code


def run_job(job_id, run_date, user_id, rerun_flag,
            schedule_id, schedulelog_id, mark_complete=False):
    """
        run the job
    """
    logging.debug('run_job for id: %s', str(job_id))
    """
        status: job_id,
        success/failure: 0 - failure, 1 success , 2 - not ready
        job object
        jobrun object
    """
    status = [job_id, 0, None, None]
    from core.controller.jobcontroller import JobController

    job_controller = JobController(
        user_id=user_id,
        job_id=job_id,
        run_date=run_date
    )

    job_controller.schedule_id = schedule_id
    job_controller.schedulelog_id = schedulelog_id
    job_controller.mark_complete = mark_complete
    try:
        return_status = job_controller.execute(
            schedule_id,
            schedulelog_id,
            rerun_flag == 'Y',
            mark_complete)
    except SIDException as exp:
        logging.error('Job failure for %s', job_id)
        logging.error(str(exp))
        status = [job_id, 0, job_controller.job, job_controller.job_run]
        return status
    """
        check the job status
        we check from DB instead of controller as job might have run before
    """
    if not return_status:
        return [job_id, 2, job_controller.job, None]

    if mark_complete:
        return [job_id, 1, job_controller.job, None]

    from core.models.coreproxy import JobrunLogProxy

    jobrun_log = JobrunLogProxy.objects.filter(
        job_id=job_id,
        run_date=run_date,
        status='Complete'
    ).order_by('-id')
    if jobrun_log:
        """
            we can do something with job run log
        """
        return [job_id, 1, job_controller.job, jobrun_log[0]]

    return status
