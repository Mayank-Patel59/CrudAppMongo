"""
Created on Saturday Sep 12 00:06:08 2020

@author: Mayank patel
"""

import json

from bson import ObjectId
from bson.json_util import dumps
from pymongo import MongoClient                                 # Pymongo API of Mongodb 
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash

app = Flask(__name__)

mongo = MongoClient("mongodb://localhost:27017/CrudRepo")        # MongoDb Connection / Database Name


# Add User Data To Mongodb
@app.route('/adduser', methods=['POST'])
def add_user():
    data = request.json
    name = data['name']
    email = data['email']
    pwd = data['pwd']
    role_id = data['role']
    if name and email and email and request.method == 'POST':
        print(request.method)
        hashed_password = generate_password_hash(pwd)
        mongo.CrudRepo.Test.insert({'name': name, 'email': email, 'pwd': hashed_password, "role": role_id})          # DatabaseName.Collection_Name.Operation
        response = jsonify('user added successfully')
        response.status_code = 200

        return response
    else:
        return not_found()


# Add role for User To Mongodb
@app.route('/addrole', methods=['POST'])
def add_roles():
    data = request.json
    role_id = data["id"]
    role = data['role']
    if role and request.method == 'POST':
        print(request.method)
        mongo.CrudRepo.TestRel.insert({'_id': role_id, 'role': role})        
        response = jsonify('user added successfully')
        response.status_code = 200

        return response
    else:
        return not_found()


# Fetch User Details From Mongodb
@app.route('/users')
def users():
    users = mongo.CrudRepo.Test.find()
    response = dumps(users)
    return response


# Fetch Roles of Users From Mongodb
@app.route('/roles')
def roles():
    roles = mongo.CrudRepo.TestRel.find()           
    response = dumps(roles)
    return response


# Search User Details by ID From Mongodb
@app.route('/user/<id>')
def user(id):
    user = mongo.CrudRepo.Test.find_one({"_id": ObjectId(id)})          
    response = dumps(user)
    return response


# Fetch Data of User Using Role
@app.route('/userRoledata/<id>')
def user_role_data(id):
    user_role_data = mongo.CrudRepo.Test.aggregate([{"$lookup": {"from": "TestRel", "localField": "role", "foreignField": "_id", "as": "TestRel"}}])       
    response = dumps(user_role_data)
    return response


# Fetch User Details By Id
@app.route('/role/<id>')
def role(id):
    role = mongo.CrudRepo.Test.find_one({"_id": ObjectId(id)})
    response = dumps(role)
    return response


# Delete User From Mongodb
@app.route('/deleteuser/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.CrudRepo.Test.delete_one({"_id": ObjectId(id)})
    response = jsonify("user deleted successfully")
    response.status_code = 200
    return response


# Delete Role of user From Mongodb
@app.route('/deleterole/<id>', methods=['DELETE'])
def delete_role(id):
    mongo.CrudRepo.TestRel.delete_one({"_id": ObjectId(id)})
    response = jsonify("role deleted successfully")
    response.status_code = 200
    return response


# Update User From Mongodb
@app.route('/updateuser/<id>', methods=['PUT'])
def update_user(id):
    _id = id
    response = request.json
    name = response['name']
    email = response['email']
    pwd = response['pwd']

    if name and email and pwd and id and request.method == 'PUT':
        hashed_password = generate_password_hash(pwd)
        mongo.CrudRepo.Test.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name': name, 'email': email, 'pwd':hashed_password}})
        resp = jsonify("user updated successfully")
        return resp


# Update Role of User
@app.route('/updaterole/<id>', methods=["PUT"])
def update_role(id):
    _id = id
    response = request.json
    role = response['role']

    if role and id and request.method == 'PUT':
        mongo.CrudRepo.Test.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                       {'$set': {'role': role}})
        resp = jsonify("role updated successfully")
        return resp


# Exception Handling 
@app.errorhandler(404)
def not_found(error=None):
    message = {'status': 404, 'message':"Not Found"+request.url}

    response = jsonify(message)
    response.status_code = 404

    return response



"""Main Function,
    Port and host details set here"""
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)        
