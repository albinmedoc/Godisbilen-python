from datetime import datetime, time
from flask import current_app

def shop_open():
    shop_open = False
    dow = str(datetime.now().weekday())
    if(dow in current_app.config["OPENING_HOURS"]):
        for time_range in current_app.config["OPENING_HOURS"][dow]:
            if(is_time_between(time_range[0], time_range[1], datetime.now().time())):
                shop_open = True
                continue
    return shop_open

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time