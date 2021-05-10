import logging

from core.general import settings
from core.general.exceptions import SIDException
from core.decorator.singleton import Singleton


class SidSettingsService(metaclass=Singleton):
    """
        Sid Settings
    """

    def __init__(self, *args, **kwargs):
        self.settings = {}
        logging.debug('sidsettingsservice: init')

        allowed_fields = set(['user_id'])
        for field in allowed_fields:
            try:
                setattr(self, field, kwargs[field].strip())
            except Exception:
                setattr(self, field, None)

        self.execute(self.user_id)

    def execute(self, user_id='system'):
        """
            fetch settings
        """
        logging.debug('sidsettingsservice: execute')
        from core.models.coreproxy import SidSettingsProxy
        records = SidSettingsProxy.objects.filter(object_owner=user_id)
        if not records and self.user_id != 'system':
            records = SidSettingsProxy.objects.filter(object_owner='system')

        for record in records:
            self.settings[record.key] = record.value

    def getkeyvalue(self, key):
        return self.settings.get(key, '')

    @property
    def sidadmin(self):
        return self.settings.get('SID_ADMIN', settings.SID_ADMIN)

    def getkeyvalue_as_num(self, key):
        value = self.getkeyvalue(key)
        try:
            value = int(value)
            return value
        except Exception as exp:
            logging.error('Invalid number for key: %s', key)
            logging.error(str(exp))
            return None
