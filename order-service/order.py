import pymysql
import time
import datetime
from flask import Flask, jsonify, request, make_response
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'bcacc0c99d9454'
app.config['MYSQL_DATABASE_PASSWORD'] = '08dac829'
app.config['MYSQL_DATABASE_DB'] = 'heroku_4482c1f4fb13bb9'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-02.cleardb.com'

mysql.init_app(app)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( {'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( {'error': 'Not found' } ), 404)

@app.route('/')
def api_root():
    return "Tubes sister tiket pesawat order service"
        
@app.route('/rpc/order', methods=['GET'])
def get_orders():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM `ORDER`"
    cursor.execute(query)
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/rpc/order/<id>', methods=['GET'])
def get_order(id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM `ORDER` WHERE `id_order` = %s"
    cursor.execute(query, id)
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/rpc/order/<id>', methods=['DELETE'])
def delete_order(id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "DELETE FROM `ORDER` WHERE `id_order` = %s"
    cursor.execute(query, id)
    conn.commit()
    return make_response(jsonify({'status': 'DELETE SUCCESS'}), 200)


@app.route('/rpc/order', methods=['POST'])
def api_add_new():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        id_order = '' + request.json['id_order']
        ts = time.time()
        order_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') 
        status = 'ACTIVE'
        id_passenger = '' + request.json['id_passenger']
        id_ticket = '' + request.json['id_ticket']
        query = "INSERT INTO `order` (`id_order`, `order_time`, `status`, `id_passenger`, `id_ticket`) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (id_order, order_time, status, id_passenger, id_ticket))
        conn.commit()
        return make_response(jsonify({'status': 'ORDER SUCCESS'}), 200)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run()
    app.debug = True
    app.run(host='0.0.0.0', port=5000)