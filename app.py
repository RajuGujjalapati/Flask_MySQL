from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from fuzzywuzzy import process
# from flask_mysqldb import MySQL
import os

#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/flask_restapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)
 
# Product Class/Model
class UserData(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  firstName = db.Column(db.String(100), unique=False)
  lastName = db.Column(db.String(200))
  gender = db.Column(db.String(10))
  dob = db.Column(db.Date)

  def __init__(self,firstName, lastName, gender, dob):
    self.firstName = firstName
    self.lastName = lastName
    self.gender = gender
    self.dob = dob

# Product Schema
class UserdataSchema(ma.Schema):
  class Meta:
    fields = ('firstName','lastName','id' ,'gender', 'dob')

# Init schema
userdata_schema = UserdataSchema() #for single product
usersdata_schema = UserdataSchema(many=True)#to deal with multiple products

# Create a User
@app.route('/postuser', methods=['POST'])
def add_product():
  firstname = request.json['firstName']
  lastname = request.json['lastName']
  gender = request.json['gender']
  dob = request.json['dob']
    #instantiating  the fileds specified while creating the database using class(variable)
  new_data = UserData(firstname, lastname, gender, dob)

  db.session.add(new_data) 
  db.session.commit()
  return userdata_schema.jsonify(new_data)

# Get All Products
@app.route('/getallusers', methods=['GET'])
def get_users():
  all_users = UserData.query.all()
  result = usersdata_schema.dump(all_users)
  return jsonify(result)
  
@app.route('/getuser/<id>', methods=['GET'])
def get_user(id):
  user = UserData.query.get(id)
  return userdata_schema.jsonify(user)

# Update a User
@app.route('/updateuser/<id>', methods=['PUT'])
def update_user(id):
  user = UserData.query.get(id)

  fname = request.json['firstName']
  lname = request.json['lastName']
  gender = request.json['gender']
  dob = request.json['dob']


  user.firstName = fname
  user.lastName = lname
  user.gender = gender
  user.dob = dob

  db.session.commit()

  return userdata_schema.jsonify(user)

# Delete Product
@app.route('/deluser/<id>', methods=['DELETE'])
def delete_user(id):
  user = UserData.query.get(id)
  db.session.delete(user)
  db.session.commit()
  return userdata_schema.jsonify(user)

# def get_match(query,choices):

# get_match("raju",get_users())
# Run Server
if __name__ == '__main__':
  app.run(debug=True)
  