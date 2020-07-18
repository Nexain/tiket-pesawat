import pymysql
import time
import datetime
from flask import Flask, jsonify, request, make_response
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'b9eb5377c92875'
app.config['MYSQL_DATABASE_PASSWORD'] = 'c784cf99'
app.config['MYSQL_DATABASE_DB'] = 'heroku_a2f54536fa7415d'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-02.cleardb.com'

mysql.init_app(app)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( {'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( {'error': 'Not found' } ), 404)

@app.route('/')
def splash():
    return 'TUBES SISTEM TERDISTRIBUSI - TIKET PESAWAT - PRODUCT SERVICE'

@app.route('/rpc')
def api_root():
    return "REMOTE PROCEDURE CALL DEMO"

@app.route('/rpc/products', methods=['GET'])
def get_products():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM TICKET"
        cursor.execute(query)
        data = cursor.fetchall()

        return jsonify(data)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/rpc/products', methods=['POST'])
def add_products():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.args is None:
            abort(400)
        id_ticket = '' + request.args['id_ticket']
        stock = '' + request.args['stock']
        price = '' + request.args['price']
        departure = '' + request.args['departure']
        arrival = '' + request.args['arrival']
        ts = time.time()
        take_off = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')   
        landing = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        query = "INSERT INTO `ticket` (`id_ticket`, `take_off`, `landing`, `stock`, `price`, `departure`, `arrival`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (id_ticket, take_off, landing, stock, price, departure, arrival))
        conn.commit()
        return make_response(jsonify({'status': 'SUCCESS'}), 200)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/rpc/products', methods=['DELETE'])
def delete_products(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if request.args is None:
                abort(400)
        id_ticket = '' + request.args['id_ticket']
        query = "DELETE FROM `ticket` WHERE `id_ticket` = %s"
        cursor.execute(query, id)
        conn.commit()
        return make_response(jsonify({'status': 'DELETE SUCCESS'}), 200)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run()
#   app.debug = True
#   app.run(host='0.0.0.0', port=5000)