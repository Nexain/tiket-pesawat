from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from sqlalchemy import and_, select
import pymysql

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://b53bb69f7b6f51:31f2b8ff@us-cdbr-east-02.cleardb.com:3306/heroku_4f332a56efa7d23'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Passenger Class/Model
class Passenger(db.Model):
    id_passenger = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(20))
    address = db.Column(db.String(100))
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))

    def __init__(self, id_passenger, name, address, username, password):
        self.id_passenger = id_passenger
        self.name = name
        self.address = address
        self.username = username
        self.password = password

# Passenger Schema
class PassengerSchema(ma.Schema):
  class Meta:
    fields = ('id_passenger', 'name', 'address', 'username', 'password')

# Init schema
passenger_schema = PassengerSchema()
passengers_schema = PassengerSchema(many=True)

@app.route('/')
def splash():
    return 'SISTER TIKET PESAWAT - CUSTOMER SERVICE'

# Add Passenger
@app.route('/rpc/passenger', methods=['POST'])
def add_passenger():
    # Get from request body
    id_passenger = request.json['id_passenger']
    name = request.json['name']        
    address = request.json['address']        
    username = request.json['username']        
    password = request.json['password']        

    # Create new passanger object
    passenger = Passenger(id_passenger, name, address, username, password)

    try:
        # add passenger
        db.session.add(passenger)
        # save changes
        db.session.commit()
        return passenger_schema.jsonify(passenger)
    except Exception as e:
        print(e)

# Get All Passenger
@app.route('/rpc/passenger', methods=['GET'])
def get_passengers():
    all_passengers = Passenger.query.all()
    result = passengers_schema.dump(all_passengers)
    return jsonify(result)

# Update Passenger
@app.route('/rpc/passenger/<id>', methods=['PUT'])
def update_passenger(id):
    passenger = Passenger.query.get(id)

    # Get from request body
    name = request.json['name']        
    address = request.json['address']        
    username = request.json['username']        
    password = request.json['password']        

    passenger.name = name
    passenger.address = address
    passenger.username = username
    passenger.password = password

    db.session.commit()

    return passenger_schema.jsonify(passenger)

# Delete Passenger
@app.route('/rpc/passenger/<id>', methods=['DELETE'])
def delete_passenger(id):
    deleted_passenger = Passenger.query.get(id)
    Passenger.query.filter(Passenger.id_passenger == id).delete()
    db.session.commit()
    return passenger_schema.jsonify(deleted_passenger)


# Select id_passenger, name, address FROM passenger 
# WHERE username == input_username
# AND password == input_password
@app.route('/rpc/verify', methods=['POST'])
def get_passenger_info():
    username = request.json['username']        
    password = request.json['password']        

    conds = [Passenger.username == username, Passenger.password == password]
    query = Passenger.query.filter(and_(*conds))
    passengers = passengers_schema.dump(query) # type(passenger) == list of dicts
    passengers = passengers[0] # type(passenger) == dict

    # get 'id_passenger', 'name', 'address'
    keys = list(['id_passenger', 'name', 'address'])
    results = {key: passengers[key] for key in passengers if key in keys} 

    return jsonify(results)

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=5000)