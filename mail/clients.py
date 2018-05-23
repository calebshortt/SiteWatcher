
import smtplib
import logging
import traceback

from settings import MAIL_SERVER_HOST, MAIL_SERVER_PORT

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class BasicWatcherClient(object):

    _mail_user = None
    _mail_pw = None
    _mail_dst = None

    _mail_host = None
    _mail_port = None

    def __init__(self, user, pw, dest, mailhost=None, mailport=None):
        self._mail_user = user
        self._mail_pw = pw
        self._mail_dst = dest if isinstance(dest, list) else [dest]
        self._mail_host = mailhost if mailhost else MAIL_SERVER_HOST
        self._mail_port = mailport if mailport else MAIL_SERVER_PORT

    def send_mail(self, msg, subject="SiteWatcher: Site Change"):

        mail_msg = "\r\n".join([
            "From: " + self._mail_user,
            "To: " + ", ".join(self._mail_dst),
            "Subject: " + subject,
            "",
            msg,
        ])

        try:
            if MAIL_SERVER_PORT == 465:
                server = smtplib.SMTP_SSL(self._mail_host, self._mail_port)
            else:
                server = smtplib.SMTP(self._mail_host, self._mail_port)

            server.ehlo()
            if not MAIL_SERVER_PORT == 465:
                server.starttls()
            server.login(self._mail_user, self._mail_pw)
            server.sendmail(self._mail_user, self._mail_dst, mail_msg)
            server.close()
        except smtplib.SMTPAuthenticationError:
            logger.error('Wrong mail username or password. Could not authenticate with mail server.')
        except Exception:
            logger.error('Unexpected Error: Failed to send mail')
