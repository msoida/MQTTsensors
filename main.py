from time import sleep

from mqttsensors import upload_sensors


def main():
    upload_sensors()
    sleep(120)
