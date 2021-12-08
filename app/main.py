from flask import Flask, jsonify
import mysql.connector
import pandas

mydb = mysql.connector.connect(user='root', password='Blue2007!',
                               host='localhost',
                               database='Talon540')

cur = mydb.cursor()

app = Flask(__name__)

db = list()

current_name = None


@app.route('/addName/<string:name>')
def addName(name):
    global current_name
    current_name = name
    print(current_name)
    if name == '':
        return {'output': False}
    else:
        return {'output': True}


@app.route('/deleteAccount/<string:deviceID>')
def deleteAccount(deviceID):
    query = f"delete from accounts where deviceID = '{deviceID}'"
    cur.execute(query)
    mydb.commit()
    query2 = 'select * from accounts'
    cur.execute(query2)
    res = cur.fetchall()
    print('database after deleting account: ', res)
    return {'success': True}


@app.route('/fetchInformation/<string:deviceID>')
def fetchInformation(deviceID):
    query = f"select * from Accounts where deviceID = '{deviceID}';"
    cur.execute(query)
    res = cur.fetchall()
    print('account:', res)
    if len(res) != 0:
        print('success')
        return {'deviceID': res[0][0],
                'name': res[0][1],
                'subgroup': res[0][2],
                'status': res[0][3],
                'gradYear': res[0][4]}
    else:
        print('fail')
        return {'output': False}


@app.route('/fetchUsername/<string:deviceID>')
def fetchUsername(deviceID):
    query = f"select * from Accounts where deviceID = '{deviceID}'"
    print('fetching username')
    cur.execute(query)
    res = cur.fetchall()
    print(res)
    if [deviceID == i[0] for i in res]:
        print(res[0][1])
        return {'name': res[0][1]}
    else:
        return {'name': False}


@app.route('/<string:subgroup>/<string:status>/<string:gradYear>/<string:deviceID>')
def storeInfo(subgroup, status, gradYear, deviceID):
    print(current_name)
    query = f"insert into Accounts(deviceID, name, subgroup, status, gradYear) " \
            f"values('{deviceID}', '{current_name}', '{subgroup}', '{status}', {gradYear})"
    try:
        cur.execute(query)
        mydb.commit()
    except:
        return {'value': False}

    if deviceID == '' or subgroup == '' or status == '' or gradYear == '':
        return {'value': False}
    else:
        return {'value': True}
