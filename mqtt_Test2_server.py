# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import serial
import time

mqttc = mqtt.Client("python_pub")
##mqttc = mqtt.Client("hello/world")
mqttc.connect("test.mosquitto.org", 1883)
##mqttc.connect("192.168.0.8", 1883)

#MQTT_Topic_Speed = "hoo/speed"
#MQTT_Topic_Distance = "hoo/distance"
#MQTT_Topic_Heartbeat = "hoo/heartbeat"

port = "/dev/ttyACM0"
serialFromArduino = serial.Serial(port, 9600)
serialFromArduino.flushInput()

def publish_To_Topic(topic, message):
    mqttc.publish(topic, message)
    print("Published : {}".format(message) + " " + "on MQTT Topic : {} ".format(topic))

#time.sleep(2)
while True:
    sum = 0
    count = 0
        
    current_time = time.time()
    end_time = time.time()
    while(True):
        input_s = serialFromArduino.readline()
        input = input_s.decode('ascii')
        heartbeat = 0
    ##    print("{}".format(input.split(" ")))
        
        if len(input) <8:
            heartbeat = input[0:3]
            print("♥♥ heart ♥♥: {}".format(heartbeat))
            mqttc.publish("hoo/heartbeat", heartbeat)
        else:
            clean_input = input.split(" ")
            distance = input[0:4]
            speed = input[5:9]
        
            print("distance : {}".format(distance) + "km "+ "speed : {}".format(speed) + "km/h " + "time : {}".format(int(time.time())))
            
            count+=1
            end_time = time.time()
            print("time : {}".format(int(end_time - current_time)))
            if (count>10):
                try:
                    ## if (type(float(speed)) == type(1.1)):
                    sum += float(speed)
                    ## print("sum : {}".format(sum))
                    if (int(end_time - current_time) > 5):
                        print("avg : {}".format(sum/(end_time - current_time)))
                except Exception:
                    pass
            
            #publish_To_Topic(MQTT_Topic_Speed, speed)
            #publish_To_Topic(MQTT_Topic_Distance, distance)
            #publish_To_Topic(MQTT_Topic_Heartbeat, heartbeat)
            mqttc.publish("hoo/speed", speed)
            mqttc.publish("hoo/distance", distance)
        
                   
        # mqttc.loop(2)
# time.sleep(2);
# mqttc.publish("hello/world", input_s)
# mqttc.loop(2)