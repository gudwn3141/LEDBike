# -*- coding: utf-8 -*-

from __future__ import print_function
import paho.mqtt.client as mqtt
import mysql.connector

## 2018.05.16(수)
## RDS 접속 확인

conn = mysql.connector.connect(user="raspberrypi", password="raspberrypi",
                             host="raspberrydb.cvlmaax7vr80.ap-northeast-2.rds.amazonaws.com",
                             database="raspberrypi", port=3306)

cursor = conn.cursor(buffered=True)
query = "SELECT name FROM user"
cursor.execute(query)

# for name in cursor:
#     print("name : {}".format(name))

MQTT_SERVER = "test.mosquitto.org"
MQTT_PATH = "hoo/#"

print("check!!")

def on_connect(client, userdata, flags, rc):
    print("connect result"+ str(rc))
    client.subscribe(MQTT_PATH)
    
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

    ## 2018.05.22(화)
    ## 평균속도 INSERT in DB
    if (msg.topic == "hoo/speed"):
        val_speed = float(str(msg.payload.decode("utf-8")))
        print("speed : ", val_speed)
        cursor.execute("""INSERT INTO speedtest (speed) VALUES (%f)""" % val_speed)
        conn.commit()

# conn.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)
client.loop_forever()
