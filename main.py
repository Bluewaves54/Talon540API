from flask import Flask, jsonify
import mysql.connector
import pandas

mydb = mysql.connector.connect(user='root', password='password',
                               host='localhost',
                               database='Talon540')

cur = mydb.cursor()

app = Flask(__name__)

db = list()


@app.before_request
def before():
    print("This is executed BEFORE each request.")


@app.route('/<string:deviceID>')
def verifyDeviceID(deviceID):
    query = f"select * from Accounts where deviceID = '{deviceID}';"
    cur.execute(query)
    res = cur.fetchall()
    print(res)
    if [deviceID == i[0] for i in res]:
        print('success')
        return {'output': True}
    else:
        print('fail')
        return {'output': False}


@app.route('/<string:subgroup>/<string:status>/<string:gradYear>/<string:deviceID>')
def storeInfo(subgroup, status, gradYear, deviceID):
    gradYear = str(gradYear)
    for charIndex in range(len(gradYear)):
        if gradYear[charIndex] == 'o':
            gradYear[charIndex] = 0

    query = f"insert into Accounts(deviceID, subgroup, status, gradYear) " \
            f"values('{deviceID}', '{subgroup}', '{status}', {gradYear})"
    cur.execute(query)
    mydb.commit()

    if deviceID == '' or subgroup == '' or status == '' or gradYear == '':
        return {'value': False}
    else:
        return {'value': True}


if __name__ == '__main__':
    app.run()
