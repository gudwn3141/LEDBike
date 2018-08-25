# -*- coding: utf-8 -*-
from __future__ import print_function
from flask import Flask, session, redirect, url_for, request, render_template, jsonify
from collections import OrderedDict

#from flask_mqtt import Mqtt
import pymysql
import datetime
import subprocess
import json


import paho.mqtt.client as mqtt
import mysql.connector
count = 0
ice = 0
weather = "weather"
val_distance =0
val_speed_avg =0
val_heartbeat = 0
cnt = 0
roro = "s1"
MQTT_SERVER = "test.mosquitto.org"
MQTT_PATH = "hoo/#"
def on_connect(client, userdata, flags, rc):
    print("connect result" + str(rc))
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):
    global count
    global roro
    global ice
    global cnt
    global val_distance
    global val_speed_avg
    global val_heartbeat
    if count<36:
        # print(msg.topic + " " + str(msg.payload))


        ## 2018.05.22(화)
        ## 평균속도 INSERT in DB
        if (msg.topic == "hoo/avg"):
            val_speed_avg = float(str(msg.payload.decode("utf-8")))

            # print("speed : ", val_speed)
            # sql0 = "SELECT * FROM speedtest order by id desc limit 1"

            # cursor.execute(sql0)
            # data = cursor.fetchall()
            conn = mysql.connector.connect(user="raspberrypi", password="raspberrypi",
                                           host="raspberrydb.cvlmaax7vr80.ap-northeast-2.rds.amazonaws.com",
                                           database="raspberrypi", port=3306)

            cursor = conn.cursor(buffered=True)
            query = "SELECT nickname, you_nickname FROM customer ORDER BY id DESC LIMIT 1"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                row1 = row[0]
                row2 = row[1]
            # if row1:
            # sqlsql = "INSERT INTO speed3(%s) WHERE nickname = %s VALUES(%s)"
            cursor.execute("UPDATE speed3 SET {} = {} WHERE nickname = '{}'".format(roro, val_speed_avg, row1))
            # print(roro, row1, val_)
            # cursor.execute(sqlsql,(row1,val_speed_avg))
            count += 1
            conn.commit()



            if row2:
                cursor.execute("SELECT {} FROM speed3 where nickname = '{}'".format(roro, row2))
                # cursor.execute(query1)
                row3 = cursor.fetchall()
                # row = row3[0]
                # if(row3):
                #     print(row3)
                # else:
                #     print("no")
                # apple = []
                # apple.append(row[0])
                # for index in range(len(row3)):
                #     apple.append(row3[index])
                # print(cnt)

                row = float(str(row3[0][0]))
                # row = apple(0)
                # row = row3[cnt]

                roro2 = int(roro[1])
                roro2 += 1
                roro = roro[0] + str(roro2)

            # for row in list:
                #
                #     if row[cnt] != None:
                #         row = row[cnt]

            if (val_speed_avg - float(row)) > 50.0:
                ice = 5
            elif (val_speed_avg - float(row)) > 40.0:
                ice = 4
            elif (val_speed_avg - float(row)) > 30.0:
                ice = 3
            elif (val_speed_avg - float(row)) > 20.0:
                ice = 2
            elif (val_speed_avg - float(row)) > 10.0:
                ice = 1
            elif (val_speed_avg - float(row)) > 0.0:
                ice = 0
            elif (val_speed_avg - float(row)) > -10.0:
                ice = -1
            elif (val_speed_avg - float(row)) > -20.0:
                ice = -2
            elif (val_speed_avg - float(row)) > -30.0:
                ice = -3
            elif (val_speed_avg - float(row)) > -40.0:
                ice = -4
            elif (val_speed_avg - float(row)) > -50.0:
                ice = -5
            # cnt+=1

            print(ice)
            if (msg.topic == "hoo/distance"):
                val_distance = float(str(msg.payload.decode(utf-8)))
                print("val_distance : {}".format(val_distance))
            if (msg.topic == "hoo/heartbeat"):
                val_heartbeat = float(str(msg.payload.decode(utf-8)))
                print("heartbeat : {}".format(val_heartbeat))
    else:
        roro = "s1"
        print("close")

## 2018.05.16(수)
## RDS 접속 확인



        # sql = "INSERT INTO speedtest(speed) VALUE(%s)"

        # cursor.execute(sql,data)
        # cursor.execute("""INSERT INTO speedtest (speed) VALUES (%f)""" % val_speed)
        # cursor.execute("""INSERT INTO speedtest WHERE rownum1 ORDER BY your_auto_increment_field DESC""" % val_speed)
        # conn.commit()


# conn.close()


app = Flask(__name__)
#mqtt = Mqtt(app)
# subprocess.Popen(
#     ["C:/Program Files/Anaconda3/python/bike/mqtt_Test2.py"],
#     stdout=subprocess.PIPE
# )
@app.route('/back')
def back() :
    return render_template('back.html')

@app.route('/user')
def showUserName():
    return render_template('user.html',
                           myteam = session['myteam'],
                           name = session['userName'],
                           gender = session['gender'],
                           age = session['age'],
                           competitor = session['competitor']
                           )


@app.route('/')
def Mode() :
    return render_template('Mode.html')

@app.route('/resister', methods=['POST' ,'GET'])
def resister():
    if request.method =='POST':
        if request.form["Mode"]=="one":
            return render_template('login_one.html')
        else:
            return render_template('login_two.html')

@app.route('/loginone', methods=['POST','GET'])
def loginone():
    global count
    global cnt
    global weather
    if request.form['play'] == 'back':
        return redirect(url_for('Mode'))
    else:

        if request.method == 'POST':
            session['userName'] = request.form['userName']
            session['gender'] = request.form['gender']
            session['age'] = request.form['age']
            session['myteam'] = request.form['myteam']
            session['competitor'] = request.form['competitor']
            # weather = request.form['weather']

            try:
                conn = pymysql.connect(host='raspberrydb.cvlmaax7vr80.ap-northeast-2.rds.amazonaws.com',
                                       user='raspberrypi',
                                       password='raspberrypi',
                                       db='raspberrypi',
                                       charset='utf8mb4'
                                       )
                curs = conn.cursor()
                sql0 = "SELECT id  FROM customer WHERE nickname=%s"
                curs.execute(sql0,request.form['competitor'])
                conn.commit()

                data = curs.fetchall()

                for row in data:
                    data = row[0]
                if data:
                    sql="INSERT INTO customer(nickname,age,gender,myteam,yourteam,you_nickname) VALUE(%s,%s,%s,%s,%s,%s)"
                    curs.execute(sql, (
                                       session['userName'],
                                       session['age'],
                                       session['gender'],
                                       session['myteam'],
                                       'yourteam',
                                       session['competitor']
                                      )
                                 )


                    ##sql2 = "ALTER TABLE ADD speedtest abcde VARCHAR(100)"
                  #  sql2 = "INSERT INTO speed3(nickname) VALUES({}) ".format(session['userName'])
                    sql2 = "INSERT INTO speed3(nickname) VALUES(%s)"
                    curs.execute(sql2, session['userName'])
                    conn.commit()

                    count =0
                    cnt = 3
                else:

                      return redirect(url_for('back'))
                conn.close()
            except:
                return redirect(url_for('back'))
            return redirect(url_for('showUserName'))
        else:
            return 'login failed'

@app.route('/logintwo', methods=['POST','GET'])
def logintwo():
    global count
    global cnt
    global weather
    if request.form['play'] == 'back':
        return redirect(url_for('Mode'))
    else:

        if request.method == 'POST':
            session['userName'] = request.form['userName']
            session['gender'] = request.form['gender']
            session['age'] = request.form['age']
            session['myteam'] = request.form['myteam']
            session['competitor'] = request.form['competitor']
            # weather = request.form['weather']
            try:
                conn = pymysql.connect(host='raspberrydb.cvlmaax7vr80.ap-northeast-2.rds.amazonaws.com',
                                       user='raspberrypi',
                                       password='raspberrypi',
                                       db='raspberrypi',
                                       charset='utf8mb4'
                                       )
                curs = conn.cursor()
                sql0 = "SELECT id FROM customer WHERE myteam=%s"
                curs.execute(sql0,request.form['competitor'])
                data = curs.fetchall()

                for row in data:
                    data = row[0]
                if data:
                    sql="INSERT INTO customer(nickname,age,gender,myteam,yourteam,you_nickname) VALUE(%s,%s,%s,%s,%s,%s)"
                    curs.execute(sql, (
                                       session['userName'],
                                       session['age'],
                                       session['gender'],
                                       session['myteam'],
                                       session['competitor'],
                                       'yournickname'
                                      )
                                 )
                    ##sql2 = "ALTER TABLE ADD speedtest abcde VARCHAR(100)"
                    # sql2 = "INSERT INTO speed3 (nickname) VALUE ({}) ".format(session['userName'])
                    # curs.execute(sql2)
                    sql2 = "INSERT INTO speed3(nickname) VALUES(%s)"
                    curs.execute(sql2, session['userName'])
                    conn.commit()
                    count = 0
                    cnt = 3
                else:

                      return redirect(url_for('back'))
                conn.close()
            except:
                return redirect(url_for('back'))
            return redirect(url_for('showUserName'))
        else:
            return 'login failed'

@app.route('/start', methods=['POST' ,'GET'])
def start():
    print("check!!")
    # if request.method == 'POST':
    #     if request.form['val'] == 'start':
    # cnt = 0
    # while cnt<20:
    global count
    global ice
    global val_distance
    # global val_heartbeat, val_distance, ice, count, weather
    global val_heartbeat
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_SERVER, 1883, 60)
    client.loop_start()

    # print(val_speed_avg)
    sensor = {}
    sensor["position"] = ice # 위치값
    sensor["distance"] = val_distance
    sensor["speed"] = val_speed_avg
    sensor["heartbeat"] = val_heartbeat
    # sensor["weather"] = weather
    if count==36:
        sensor["count"] = "stop"
    data = json.dumps(sensor)
    # print(data)

    #     cnt+=1
    #     print(cnt)
    # client.loop_stop()
    # return  render_template("start.html", candy = data)
    # return(redirect(url_for('showUserName')),json.dumps(sensor, ensure_ascii = False, indent ="\t"))
    return render_template('user.html',
                           myteam=session['myteam'],
                           name=session['userName'],
                           gender=session['gender'],
                           age=session['age'],
                           competitor=session['competitor']
                          ,string=data)



app.secret_key = 'abcdefgadsjflkjsdljjdlsjfkja'

if __name__ == "__main__":
    app.run()

## host='0.0.0.0', port=5002, debug=True
