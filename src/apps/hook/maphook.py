"""
  Description:    Map Hook
"""


class MapHook():
    """
        Map Hook
    """

    # def __init__(self, *args, **kwargs):

    def map(self, job_id, key, value):
        """
            jobconfig: job id
            key: field name
            value: field value
            return: new field value or none
        """
        return value
