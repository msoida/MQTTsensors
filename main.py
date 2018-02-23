from datetime import datetime, timedelta
from time import sleep

from pytz import utc

from mqttsensors import upload_list


upload_times = [datetime(1970, 1, 1, tzinfo=utc)] * len(upload_list)


def main():
    for i, ul in enumerate(upload_list):
        if datetime.now(utc) > (upload_times[i] + timedelta(seconds=ul[0])):
            for f in ul[1]:
                f()
            upload_times[i] = datetime.now(utc)
    sleep(1)
