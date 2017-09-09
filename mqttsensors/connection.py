from atexit import register as atexit
from datetime import datetime
from io import BytesIO
from json import dumps as json

from paho.mqtt.client import Client, connack_string, error_string
from PIL import (Image, ImageDraw, ImageFont)
from pytz import timezone

from .settings import status_topic, inconsolata_path


tz = timezone('Europe/Warsaw')

status_error = json(dict(status='error', value=-1))
status_connected = json(dict(status='connected', value=1))
status_disconnected = json(dict(status='disconnected', value=0))


def on_connect(client, userdata, flags, rc):
    print('MQTT connect: {}'.format(connack_string(rc)))


def on_disconnect(client, userdata, rc):
    print('MQTT disconnect: {}'.format(error_string(rc)))


def on_message(client, userdata, message):
    pass  # not used


client = Client()
client.will_set(status_topic, status_error, retain=True)
# client.connect_async('localhost')
client.connect('localhost')
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.publish(status_topic, status_connected, retain=True)
client.loop_start()


@atexit
def run_at_exit():
    client.publish(status_topic, status_disconnected, retain=True)
    client.loop_stop()
    client.disconnect()


def publish(topic, value):
    data = json(dict(value=value))
    result, mid = client.publish(topic, data, retain=True)


def upload_camera(topic, title, fntsize, bgsize, bgcolor, data):
    current_time = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
    origfile = BytesIO(data)
    img = Image.open(origfile).convert('RGBA')
    txt = Image.new('RGBA', img.size, (255, 255, 255, 0))
    fnt = ImageFont.truetype(inconsolata_path, fntsize)
    d = ImageDraw.Draw(txt)
    d.rectangle([(0, 0), bgsize], fill=bgcolor)
    d.text((5, 0), current_time, font=fnt, fill=(255, 255, 255, 255))
    d.text((5, int(fntsize * 0.9)), title, font=fnt, fill=(255, 255, 255, 255))
    out = Image.alpha_composite(img, txt)
    output = BytesIO()
    out.convert('RGB').save(output, 'JPEG')
    del img, txt
    origfile.close()
    photo = output.getvalue()
    result, mid = client.publish(topic, photo, retain=False)
