from flask_cors import CORS
from flask import Flask
from flask import request
from flask_mysqldb import MySQL
import jwt
import json
import time
import datetime



app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'satish'
app.config['MYSQL_DB'] = 'pos_app'
mysql = MySQL(app)
CORS(app)






@app.route('/login',methods=['POST'])
def login():
    email = request.json["email"]
    password=request.json["password"]
    role=request.json["role"]
    
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM auth WHERE email="%s" AND password="%s" AND role="%s";'''%(email,password,role))
    result = cur.fetchall()
    data = []
    for row in result:
        data.append(row)

    if data:
        payload = {'username': email, 'message': 'logged_in','expires':time.time()+100000000}
        key = 'secret'

        encode_jwt = jwt.encode(payload, key)

        return {'auth_token': encode_jwt.decode(), 'message': 'logged_in','role':role}
    else:
        return {'message': 'username or password incorrect'}



@app.route('/checklogin',methods=['POST'])
def check_login():
    token = request.json["auth_token"]
    decode_jwt = jwt.decode(token,"secret")
  
    if decode_jwt.get('expires')>=time.time():
        return json.dumps({'auth_token': "valid",'expires':decode_jwt.get('expires'),'time':time.time()})
    else:
        return json.dumps({'auth_token': "invalid"})



@app.route("/employee/get_stocks")
def get_stocks():
    page = request.args.get('page',type=int)
    per_page=request.args.get('per_page',type=int)
    cur = mysql.connection.cursor()
    cur.execute('''SELECT id,title,price,stock,status FROM stocks LIMIT %d,%d;'''%(page*per_page,per_page))
    result = cur.fetchall()
    data = []
    for row in result:
        data.append(row+(1,))

    return json.dumps(data)

@app.route("/employee/generate_bill",methods=['POST'])
def generate_bill():
    bill_items = request.json[0]
    bill_amount = request.json[1]
    
    for item in bill_items:
        cur = mysql.connection.cursor()
        cur.execute('''UPDATE stocks SET stock="%d" WHERE id="%d"''' % (item[3], item[0]))
        cur.execute('''UPDATE stocks SET status="%s" WHERE stock<="%d"''' % ("ordered", 10))
        mysql.connection.commit()
        cur.close()
    
    cur1 = mysql.connection.cursor()
    cur1.execute('''INSERT INTO bills(amount,generated_at) values("%d","%s")''' % (bill_amount,datetime.datetime.now()))
    mysql.connection.commit()
    cur1.close()

    return json.dumps(bill_items)

@app.route("/bills")
def get_bills():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT amount,HOUR(generated_at),MINUTE(generated_at) FROM bills''')
    result = cur.fetchall()
    x_axis = []
    y_axis=[]
    for row in result:
        x_axis.append(str(row[1]) + ":" + str(row[2]))
        y_axis.append(row[0])

    return json.dumps({"x_axis":x_axis,"y_axis":y_axis})


# @app.route('/logout',methods=['POST'])
# def logout():
#     token = request.json["auth_token"]
#     decode_jwt = jwt.decode(token,"secret")
  
#     decode_jwt['expires']= time.time()
#     return {"message":"logout success"}
      

