from datetime import datetime, time
import requests
from flask import current_app

def shop_open():
    shop_open = False

    # Check standard opening hours
    dow = str(datetime.now().weekday())
    if(dow in current_app.config["OPENING_HOURS"]):
        for time_range in current_app.config["OPENING_HOURS"][dow]:
            if(is_time_between(time_range[0], time_range[1], datetime.now().time())):
                shop_open = True
                continue

    # Check extra opening hours
    current_date = datetime.now().date()
    if(current_date in current_app.config["EXTRA_OPENING_HOURS"]):
        for time_range in current_app.config["EXTRA_OPENING_HOURS"][current_date]:
            if(is_time_between(time_range[0], time_range[1], datetime.now().time())):
                shop_open = True
                continue

    return shop_open

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current time
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def send_sms(msg, to, from_="Godisbilen", customid=None):
    URL = "https://api.budgetsms.net/sendsms/"
    to = "46" + to[1:]
    data = {
        "username": current_app.config["SMS_USERNAME"],
        "userid": current_app.config["SMS_USERID"],
        "handle": current_app.config["SMS_HANDLE"],
        "msg": msg,
        "from": from_,
        "to": to
    }

    if(customid):
        data["customid"] = customid

    r = requests.post(url=URL, data=data)
    return r.status_code