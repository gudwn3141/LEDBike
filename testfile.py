from flask import Flask, session, redirect, url_for, request, render_template
import pymysql

app = Flask(__name__)
conn = pymysql.connect(host='raspberrydb.cvlmaax7vr80.ap-northeast-2.rds.amazonaws.com',
                       user='raspberrypi',
                       password='raspberrypi',
                       db='raspberrypi',
                       charset='utf8mb4'
                       )
curs = conn.cursor()

@app.route('/user')
def showUserName():
    return render_template('user.html',
                           myteam = session['myteam'],
                           name = session['userName'],
                           person = session['people'],
                           age = session['age'],
                           competitor = session['competitor']
                           )

@app.route('/')
def login_form() :
    return render_template('login_form.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        session['myteam']=request.form['myteam']
        session['userName']=request.form['userName']
        session['people'] = request.form['person']
        session['age'] = request.form['age']
        session['competitor'] = request.form['competitor']

        sql="INSERT INTO user(name,nickname,gender,age,mode) VALUE(%s,%s,%s,%s,%s)"
        curs.execute(sql, (session['myteam'],
                           session['userName'],
                           session['people'],
                           session['age'],
                           session['competitor']
                          )
                     )
        ##sql2 = "ALTER TABLE ADD speedtest abcde VARCHAR(100)"
        sql2 = "ALTER TABLE speedtest ADD {} VARCHAR(100)".format(session['userName'])
        curs.execute(sql2)
        conn.commit()
        conn.close()
        return redirect(url_for('showUserName'))
    else:
        return 'login failed'

app.secret_key = 'abcdefgadsjflkjsdljjdlsjfkja'

if __name__ == "__main__":
    app.run()

## host='0.0.0.0', port=5002, debug=True
