"""
  Description:    helper module for different apps
"""
import os
from dateutil import tz
from datetime import datetime, date
from collections import OrderedDict

from core.general.exceptions import SIDException
from core.general import settings

def clean_string(i_string):
    """
        clean function to clean unwanted characters
        i_string: string to clean
    """
    unCharSet = {'\\': ' ', "'": '', '(': ' ', ')': ' ',
                 '.': ' ', ',': ' ', '&': ' and '}

    if i_string is None:
        return None

    for key, value in unCharSet.items():
        i_string = i_string.replace(key, value)

    o_string = i_string.split()

    o_string = " ".join(o_string)
    return o_string


def cleanfield(value):
    """
        remove spaces
    """
    # values like 0 should not be converted to None
    if value is None or value.strip() == "":
        return None
    value = str(value)
    value = value.strip()
    return value


def compare_fields(field1, field2):
    """
        compare 2 fields if they are same then return true
    """
    if field1 is None and field2 is None:
        return True

    if (field1 is None and field2 is not None) or\
            (field2 is None and field1 is not None):
        return False

    if field1 == field2:
        return True

    return False


def convert_timezone(time):
    """
        matdatepicker returns a datetime object in UTC time.
        Need to convert this to local time as only date is stored in db
    """
    if time is None:
        return None
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    try:
        utc = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        try:
            utc = datetime.strptime(time, "%Y-%m-%d")
        except ValueError:
            return None

    if utc.year < 1900 or utc.year > 9999:
        return None

    utc = utc.replace(tzinfo=from_zone)
    local_date = utc.astimezone(to_zone).date()
    return local_date


def validate_date(date_text):
    time = date_text.strip()
    try:
        datetime.strptime(time, '%Y-%m-%d')
        return True
    except ValueError:
        try:
            datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
            return True
        except ValueError:
            return False


def check_dateformat(date_field, date_format='YYYY-MM-DD'):
    """
        check the date format field
    """
    if not date_format or not date_field:
        return None
    # format = "%Y-%m-d"
    date_field = date_field.strip()

    try:
        dd = None
        mm = None
        yyyy = None
        seperator = '-'
        date_part = date_field
        time_part = None
        if '/' in date_field:
            seperator = '/'
        if ' ' in date_field:
            (date_part, time_part) = date_field.split(' ')

        if not time_part:
            if date_format == 'DD-MM-YYYY' or date_format == 'DD/MM/YYYY':
                (dd, mm, yyyy) = date_part.split(seperator)
            elif date_format == 'YYYY-MM-DD' or date_format == 'YYYY/MM/DD':
                (yyyy, mm, dd) = date_part.split(seperator)
            elif date_format == 'YYYY-DD-MM' or date_format == 'YYYY/DD/MM':
                (yyyy, dd, mm) = date_part.split(seperator)
            yyyy = int(yyyy)
            dd = int(dd)
            mm = int(mm)
            date_part = date(yyyy, mm, dd)
            return date_part
        else:
            raise SIDException(
                'Invalid Date: datetime not supported', 'datetime')
        # to support further "%d/%m/%Y %H:%M:%S"

        # date_string = str(yyyy) + '-' + str(mm) + '-' + str(dd)
        # return datetime.strptime(date_string, format)

    except Exception:
        raise SIDException('Invalid Date', 'check_dateformat')


def generate_dateformat(date_field, date_format):
    """
        check the date format field
    """
    if not date_format or not date_field:
        return None

    date_part = None
    try:
        if date_format == 'DDMMYYYY':
            date_part = date_field.strftime('%d%m%Y')
        elif date_format == 'MMDDYYYY':
            date_part = date_field.strftime('%m%d%Y')
        elif date_format == 'YYYYMMDD':
            date_part = date_field.strftime('%Y%d%m')
        elif date_format == 'YYYYDDMM':
            date_part = date_field.strftime('%Y%d%m')
    except Exception:
        raise SIDException('Invalid Date', '')

    return date_part


def remove_futuredate(date_field, date_format):
    """
        check the date format field
    """
    newdate = check_dateformat(date_field, date_format)
    if not newdate:
        raise SIDException('Invalid Date')


def setup_logfile():
    """
        function is to create log file
        it should be called from django api
        regular batch job should not use this function
    """
    from core.general.appinit import log_init
    log_init(
        'general',
        'django_api'
    )


def generate_filename(
        filepath,
        filestartwith,
        fileendwith,
        run_date,
        filemask):
    """
        generate filename based on rundate and filemask
    """

    filedate = generate_dateformat(run_date, filemask)
    if not filedate:
        filename = filestartwith
    else:
        filename = filestartwith + filedate

    if fileendwith:
        filename = filename + fileendwith

    if filepath and len(filepath.strip()) > 0:
        filename = filepath.strip() + '/' + filename

    return filename


def convert_field(field_name,
                  field_type=None,
                  field_length=None,
                  label=None,
                  primary_key=None,
                  choices=None,
                  nullable=None,
                  model_name=''
                  ):
    return {
        'field_name': field_name,
        'field_type': field_type,
        'field_length': field_length,
        'label': label,
        'primary_key': primary_key,
        'choices': choices,
        'nullable': nullable,
        'model_name': model_name
    }


def get_downloadpath(user_id):
    """
        find the download path
    """
    path = settings.DOCUMENT_PATH + str(user_id) + '/'
    if not os.path.isdir(path):
        os.mkdir(path)
    return path
