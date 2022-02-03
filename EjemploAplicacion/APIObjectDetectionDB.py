from flask import Flask, request, json, Response
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId
from datetime import datetime
import logging as log

app = Flask(__name__)
client = MongoClient("mongodb://mongo_db:27017/")
db = client['objectdetectiondb']
collection = db['images']
db2 = client['webdb']
collection2 = db2['users']

@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')


@app.route('/readImages', methods=['GET'])
def readImages():
    """data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')"""
    result = collection.find()
    response = json_util.dumps(result)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

@app.route('/readUsers', methods=['GET'])
def readUsers():
    """data = request.json
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')"""
    result = collection2.find()
    response = json_util.dumps(result)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app.route('/saveImage', methods=['POST'])
def writeImage():
    imageName = request.form['imageName']
    imageDate = request.form['imageDate']
    imageProcDate = datetime.now().strftime('%Y/%m/%d-%H:%M:%S:%f')
    imageBytes = request.form['imageBytes']

    if imageName and imageBytes:
        response = collection.insert_one({'imageName':imageName, 'imageDate': imageDate, 'imageProcDate': imageProcDate, 'imageBytes': imageBytes})
        #response = collection.insert_one({'imageName':imageName, 'imageBytes': imageBytes})
        if response:
            return Response(response=json.dumps({"Message": "Correct insertion"}),
                        status=200,
                        mimetype='application/json')
        else:
            return Response(response=json.dumps({"Error": "Something wrong during insertion"}),
                        status=400,
                        mimetype='application/json')
    else:
        return Response(response=json.dumps({"Error": "Some field is empty"}),
                        status=400,
                        mimetype='application/json')
        
@app.route('/saveUser', methods=['POST'])
def writeUser():
    userName = request.form['userName']
    userEmail = request.form['userEmail']

    if userName and userEmail:
        results = collection2.count_documents({'userEmail': userEmail})
        if results <=0:
            response = collection2.insert_one({'userName':userName, 'userEmail': userEmail})
            if response:
                return Response(response=json.dumps({"Message": "Correct insertion"}),
                            status=200,
                            mimetype='application/json')
            else:
                return Response(response=json.dumps({"Error": "Something was wrong during insertion"}),
                            status=400,
                            mimetype='application/json')
        else:
            return Response(response=json.dumps({"Message": "User is already registered"}),
                            status=200,
                            mimetype='application/json')

    else:
        return Response(response=json.dumps({"Error": "Some field is empty"}),
                        status=400,
                        mimetype='application/json')
        

@app.route('/deleteImage', methods=['DELETE'])
def deleteImage():
    imageName = request.form['imageName']
    if imageName:

        response = collection.delete_one({'imageName': imageName})
        if response:
            return Response(response=json.dumps({"Message": "Image Deleted Succesfully"}),
                        status=200,
                        mimetype='application/json')
        else:
            return Response(response=json.dumps({"Error": "Something was wrong during deleted"}),
                        status=400,
                        mimetype='application/json')
    else:
        return Response(response=json.dumps({"Error": "Some field is empty"}),
                        status=400,
                        mimetype='application/json')

@app.route('/deleteUser', methods=['DELETE'])
def deleteUser():
    email = request.form['userEmail']
    if email:
        response = collection2.delete_one({'userEmail': email})
        if response:
            return Response(response=json.dumps({"Message": "User Deleted Succesfully"}),
                        status=200,
                        mimetype='application/json')
        else:
            return Response(response=json.dumps({"Error": "Something was wrong during deleted"}),
                        status=400,
                        mimetype='application/json')
    else:
        return Response(response=json.dumps({"Error": "Some field is empty"}),
                        status=400,
                        mimetype='application/json')



if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')


