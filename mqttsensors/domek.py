from requests import get as urlget
from requests.exceptions import RequestException

from bme280 import BME280, BME280Error

from .connection import publish, upload_camera
from .settings import (temp_topic, humid_topic, press_topic,
                       ogrodcam_topic, podjazdcam_topic,
                       ogrodcam_url, podjazdcam_url)


bme = BME280()
bme.set_acquisition_options(16, 16, 2, 16)
bme.set_config(1000, 16)


def upload_attic():
    try:
        temp = bme.temperature()
        humid = bme.humidity()
        press = bme.pressure()
    except BME280Error:
        print('Sensor error')
        return
    publish(temp_topic, temp)
    publish(humid_topic, humid)
    publish(press_topic, press)


def get_cam_data(url):
    try:
        response = urlget(url, timeout=10)
        if not response.ok:
            raise RequestException
        orig = response.content
    except RequestException:
        print('RequestException - get data')
        return
    return orig


def upload_ogrodcam():
    title = 'Ogród'
    url = ogrodcam_url
    topic = ogrodcam_topic
    data = get_cam_data(url)
    # upload_camera(topic, title, 22, (220,50), (0,0,0,128), data)
    upload_camera(topic, title, 22, (300, 50), (75, 75, 75, 255), data)


def upload_podjazdcam():
    title = 'Podjazd'
    url = podjazdcam_url
    topic = podjazdcam_topic
    data = get_cam_data(url)
    # upload_camera(topic, title, 22, (220, 50), (0, 0, 0, 128), data)
    upload_camera(topic, title, 22, (300, 50), (75, 75, 75, 255), data)


upload_list = [
    (60, [upload_ogrodcam, upload_podjazdcam]),
    (120, [upload_attic]),
]
