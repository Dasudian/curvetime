import uuid
import time
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from curvetime.utils import ecode



def utc_to_timestamp(s):
    return int(datetime.strptime(s, '%Y-%m-%d %H:%M:%S').strftime("%s"))


def timestamp_to_utc(t):
    return datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')

def is_weekend():
    td = datetime.today().weekday()
    if td == 5 or td == 6:
        return True
    elif td == 0:
        if datetime.now().hour < 9:
            return True
        else:
            return False
    else:
        return False


def util_response(data='', code=ecode.SUCCESS, http_status=status.HTTP_200_OK):
    if http_status == status.HTTP_200_OK:
        if data == []:
            return Response({"code": code, "msg": ecode.ErrorCode[code], "data": data})
        elif data:
            return Response({"code": code, "msg": ecode.ErrorCode[code], "data": data})
        else:
            return Response({"code": code, "msg": ecode.ErrorCode[code]})
    else:
        return Response({"code": http_status, "msg": data if data else ecode.ErrorCode.get(http_status, 'error')},
                        status=http_status)



def send_email(to, code):
    msg = """From: No-Reply <noreply@dasudian.com>
    MIME-Version: 1.0
    Content-type: text/html
    Subject: curvetime

    this is your message"""

    try:
        smtp = smtplib.SMTP('mail.dasudian.com')
        smtp.login('noreply@dasudian.com', 'xxxxxxxxx')
        smtp.sendmail('noreply@dasudian.com', to, msg)
        smtp.quit()
    except smtplib.SMTPException as e:
        print(e)
        smtp.quit()
