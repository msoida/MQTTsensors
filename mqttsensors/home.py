from subprocess import run, PIPE, SubprocessError

from bmp280 import BMP280, BMP280Error
from bme280 import BME280, BME280Error
from am2315 import AM2315, AM2315Error

from .connection import publish, upload_camera
from .settings import (bmp_temp_topic, bmp_press_topic,
                       bme_temp_topic, bme_press_topic, bme_humid_topic,
                       out_temp_topic, out_humid_topic,
                       raspicam_topic)


raspicam = ['raspistill', '-n', '-vf', '-hf',
            '-t', '1000', '-br', '55', '-o', '-']

bmp = BMP280()
bmp.set_acquisition_options(16, 16, 2)
bmp.set_config(1000, 16)

bme = BME280(alternativeAddress=True)
bme.set_acquisition_options(16, 16, 2, 16)
bme.set_config(1000, 16)

out = AM2315(bus=3)


def upload_bmp():
    try:
        BMPtemperature = bmp.temperature()
        BMPpressure = bmp.pressure(update_temperature=False)
    except BMP280Error:
        print('BMP280 Error')
        return
    publish(bmp_temp_topic, BMPtemperature)
    publish(bmp_press_topic, BMPpressure)


def upload_bme():
    try:
        BMEtemperature = bme.temperature()
        BMEpressure = bme.pressure(update_temperature=False)
        BMEhumidity = bme.humidity(update_temperature=False)
    except BME280Error:
        print('BME280 Error')
        return
    publish(bme_temp_topic, BMEtemperature)
    publish(bme_press_topic, BMEpressure)
    publish(bme_humid_topic, BMEhumidity)


def upload_out():
    try:
        temperature = out.temperature()
        humidity = out.humidity()
    except AM2315Error:
        print('AM2315 Error')
        return
    publish(out_temp_topic, temperature)
    publish(out_humid_topic, humidity)


def upload_picam():
    try:
        proc = run(raspicam, check=True, stdout=PIPE, timeout=10)
    except SubprocessError:
        print('PiCam Error')
        return
    data = proc.stdout
    t = raspicam_topic
    upload_camera(t, 'PiCam', 45, (450, 100), (0, 0, 0, 128), data)


upload_list = [
    (60, [upload_picam]),
    (120, [upload_bmp, upload_bme, upload_out]),
]
