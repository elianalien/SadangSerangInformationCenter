from datetime import datetime, timedelta
import time

# Bismillahirrahmanirrahim

def to_friendly_time(time_then_text):
    time_then = datetime.strptime(time_then_text, '%Y-%m-%d %H:%M:%S')
    time_local_now = datetime.fromtimestamp(time.time())
    time_diff = time_local_now - time_then

    result = ""

    if time_diff.days >= 3 :
        result = time_then.strftime('%Y-%m-%d %H:%M:%S')

    elif time_diff.days > 0 :
        result = str(time_diff.days) + " hari yang lalu"

    elif time_diff.seconds >= 3600 :
        result = str(int(time_diff.seconds/3600)) + " jam yang lalu"

    elif time_diff.seconds >= 60:
        result = str(int(time_diff.seconds/60)) + " menit yang lalu"

    else:
        result = str(time_diff.seconds) +" detik yang lalu"

    return result










