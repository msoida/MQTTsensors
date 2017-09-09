from decouple import config


location = config('LOCATION')
status_topic = config('STATUS_TOPIC')
inconsolata_path = config('INCONSOLATA_PATH')

if location == 'home':
    bmp_temp_topic = config('BMP_TEMP_TOPIC')
    bmp_press_topic = config('BMP_PRESS_TOPIC')
    bme_temp_topic = config('BME_TEMP_TOPIC')
    bme_press_topic = config('BME_PRESS_TOPIC')
    bme_humid_topic = config('BME_HUMID_TOPIC')
    out_temp_topic = config('OUT_TEMP_TOPIC')
    out_humid_topic = config('OUT_HUMID_TOPIC')
    raspicam_topic = config('RASPICAM_TOPIC')
    out_ip = config('OUT_IP')
    out_port = config('OUT_PORT',cast=int)

elif location == 'domek':
    temp_topic = config('TEMP_TOPIC')
    humid_topic = config('HUMID_TOPIC')
    press_topic = config('PRESS_TOPIC')
    ogrodcam_topic = config('OGRODCAM_TOPIC')
    podjazdcam_topic = config('PODJAZDCAM_TOPIC')
    ogrodcam_url = config('OGRODCAM_URL')
    podjazdcam_url = config('PODJAZDCAM_URL')
