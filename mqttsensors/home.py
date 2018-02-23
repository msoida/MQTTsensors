
from json import loads as unjson
from socket import socket
from subprocess import run, PIPE
from time import sleep

from bmp280 import BMP280, BMP280Error
from bme280 import BME280, BME280Error
from ina219 import INA219, INA219Error

from .connection import publish, upload_camera
from .settings import (bmp_temp_topic, bmp_press_topic, bme_temp_topic,
                       bme_press_topic, bme_humid_topic, out_temp_topic,
                       out_humid_topic, raspicam_topic, out_ip, out_port,
                       ina_voltage_topic, ina_power_topic, ina_current_topic)


raspicam = ['raspistill', '-n', '-vf', '-hf',
            '-t', '1000', '-br', '55', '-o', '-']

bmp = BMP280()
bmp.set_acquisition_options(16, 16, 2)
bmp.set_config(1000, 16)

bme = BME280(alternativeAddress=True)
bme.set_acquisition_options(16, 16, 2, 16)
bme.set_config(1000, 16)

ina = INA219()
ina.shuntADC(128)
ina.busADC(128)
ina.vrange(16)
ina.set_calibration()


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


def upload_ina():
    try:
        INAvoltage = ina.bus_voltage()
        INApower = ina.power()
        INAcurrent = ina.current()
    except INA219Error:
        print('INA219 Error')
        return
    publish(ina_voltage_topic, INAvoltage)
    publish(ina_power_topic, INApower)
    publish(ina_current_topic, INAcurrent)


def upload_out():
    s = socket()
    s.connect((out_ip, out_port))  # Connect to sensor
    s.send(b'\0')  # Trigger sensor output
    sleep(0.1)  # Wait for full response
    bdata = s.recv(1024)  # Save raw JSON bytes
    s.close()
    sdata = bdata.decode()  # Decode JSON to str
    data = unjson(sdata)
    temperature = data['temperature']
    humidity = data['humidity']
    publish(out_temp_topic, temperature)
    publish(out_humid_topic, humidity)


def upload_picam():
    proc = run(raspicam, check=True, stdout=PIPE)
    data = proc.stdout
    t = raspicam_topic
    upload_camera(t, 'PiCam', 45, (450, 100), (0, 0, 0, 128), data)


upload_list = [
    (30, [upload_ina]),
    (60, [upload_picam]),
    (120, [upload_bmp, upload_bme, upload_out]),
]
