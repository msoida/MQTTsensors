from bme280 import BME280, BME280Error
from ina219 import INA219, INA219Error
from tsl2561 import TSL2561, TSL2561Error

from .connection import publish
from .settings import (bme_temp_topic, bme_press_topic, bme_humid_topic,
                       ina_voltage_topic, ina_power_topic, ina_current_topic,
                       tsl_light_topic,
                       out_temp_topic, temp_probe_id)


bme = BME280(alternativeAddress=True)
bme.set_acquisition_options(16, 16, 2, 16)
bme.set_config(1000, 16)

ina = INA219()
ina.shuntADC(128)
ina.busADC(128)
ina.vrange(16)
ina.set_calibration()

tsl = TSL2561()
tsl.power()
tsl.timing(gain=16)

temp_probe_path = '/sys/bus/w1/devices/{}/w1_slave'.format(temp_probe_id)


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


def upload_tsl():
    try:
        TSLlight = tsl.visible()
    except TSL2561Error:
        print('TSL2561 Error')
        return
    publish(tsl_light_topic, TSLlight)


def upload_out():
    try:
        with open(temp_probe_path) as f:
            crc = f.readline()
            temp = f.readline()

    except IOError:
        temperature = None

    else:
        crc = crc.strip().split(' ')[-1]
        temp = temp.strip().split(' ')[-1][2:]
        temp = float(temp) / 1000
        temperature = (temp if crc == 'YES' else None)

    if temperature is not None:
        publish(out_temp_topic, temperature)


upload_list = [
    (30, [upload_ina]),
    (120, [upload_bme, upload_out, upload_tsl]),
]
