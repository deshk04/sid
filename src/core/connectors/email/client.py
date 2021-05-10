"""
  Description:    Operational module to send emails
"""

import os
from os.path import basename
import logging

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class SIDEmail():
    """
        Email client to send message
    """

    def __init__(self, *args, **kwargs):
        self.server = os.getenv("EMAILSERVER", '')
        self.port = 25
        self.username = os.getenv("EMAILUSER", '')
        self.password = os.getenv("EMAILPASSWORD", '')
        self.to_list = None
        self.from_list = None
        self.cc_list = None

    def __enter__(self):
        """
            method to connect to server
        """
        self.conn = smtplib.SMTP(self.server, self.port)
        if self.conn:
            self.conn.login(self.username, self.password)
        return self

    def send(self, i_subject, i_message, attachfile=None):
        """
            send email
        """

        if not self.to_list:
            logging.debug('user email not found')
            return

        from core.services.sidsettings import SidSettingsService
        sid_settings = SidSettingsService(
            user_id=self.user_id
        )

        msg = MIMEMultipart('alternative')
        self.from_list = sid_settings.getkeyvalue('EMAIL_FROM')
        self.cc_list = sid_settings.getkeyvalue('EMAIL_SUPPORT')
        msg['Subject'] = sid_settings.getkeyvalue('EMAIL_SUBJECT_PREFIX') + ' ' + i_subject
        msg['From'] = ', '.join(self.from_list)
        self.to_list = self.to_list.split(',')
        msg['To'] = ', '.join(self.to_list)

        email_list = self.to_list

        if self.cc_list:
            msg['cc'] = self.cc_list
            email_list = self.to_list + self.cc_list

        msg.add_header('Content-Type', 'text/html')
        message = MIMEText(i_message, 'html')

        msg.attach(message)

        """
            attach file if it exits
        """
        if attachfile:
            if isinstance(attachfile, list):
                for fil in attachfile:
                    with open(fil, "rb") as ofile:
                        part = MIMEApplication(
                            ofile.read(), Name=basename(fil))
                    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(
                        fil)
                    msg.attach(part)
            else:
                with open(attachfile, "rb") as ofile:
                    part = MIMEApplication(
                        ofile.read(), Name=basename(attachfile))
                    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(
                        attachfile)
                    msg.attach(part)

        self.conn.sendmail(self.from_list, email_list, msg.as_string())

    def __exit__(self, type, value, traceback):
        if self.conn:
            self.conn.quit()
