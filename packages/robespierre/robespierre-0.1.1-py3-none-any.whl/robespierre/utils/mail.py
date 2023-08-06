import logging
import smtplib
import robespierre.models as models
from typing import List


def send_mail(main_config: models.MainConfig, file_list: List[str], rcpt_list: List[str] = None):
    from_addr = main_config.config.email.sender
    passwd = main_config.config.email.password
    use_tls = main_config.config.email.use_tls
    if not rcpt_list:
        rcpt_list = main_config.config.email.default_recipients

    msg: str = ""
    for file in file_list:
        with open(file, "r") as f:
            msg += "\n" + "\n".join(f.readlines())

    logging.info("Sending mail to {}, from {}.".format(rcpt_list, from_addr))

    smtp = None
    try:
        if use_tls:
            smtp = smtplib.SMTP_SSL(host=main_config.config.email.relay_host, port=main_config.config.email.relay_port)
        else:
            smtp = smtplib.SMTP_SSL(host=main_config.config.email.relay_host, port=main_config.config.email.relay_port)
            smtp.starttls()

        smtp.login(from_addr, passwd)
        smtp.sendmail(from_addr=from_addr, to_addrs=rcpt_list, msg=msg)
    except smtplib.SMTPAuthenticationError:
        logging.exception("Failed to authenticate to server")
    except smtplib.SMTPConnectError:
        logging.exception("Failed to connect to server")
    except smtplib.SMTPException:
        logging.exception("Failed to send mail")
    finally:
        if smtp:
            smtp.close()
