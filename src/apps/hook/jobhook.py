"""
  Description:    Jobs Hook
"""
from core.general.exceptions import SIDException


class JobHook():
    """
        Job Hook
    """

    # def __init__(self, *args, **kwargs):

    def map(self, job):
        """
            job: job record
        """
        raise SIDException('Adhoc job not supported yet')

    def reader(self, user_id, run_date, job):
        """
            will return a connector similar to connector.Reader
        """
        """
            below is sample code to return a connector
        """
        if job.job_id == -999:
            """
                from apps.hook.connector.jobreader import Reader
                return Reader(
                    user_id = self.user_id,
                    run_date=self.run_date,
                    config=config
                )
            """
            from apps.hook.connector.template_reader import Reader
            reader = Reader(
                user_id=self.user_id,
                run_date=self.run_date
            )
            return reader

        raise SIDException('Adhoc reader for this job not supported')
