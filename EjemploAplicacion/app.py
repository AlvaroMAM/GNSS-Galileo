from flask import Flask, render_template, redirect, request, Response
import jinja2
import requests
import json
import numpy as np
from cv2 import cv2
from bson import json_util
import aux
import base64

app = Flask(__name__)

currentUser = aux.User("","")
myImages = []
@app.route('/')
def index():
    return render_template("index.html",user=currentUser)

@app.route('/logout')
def logout():
    currentUser.disconnect()
    return redirect('/')
    
@app.route('/login', methods=['POST'])
def login():
    #recibir datos de google oauth
    email = request.form["userEmail"]
    name = request.form["userName"]
    if(currentUser.loginOrRegister(name,email)):
        return Response(response=json.dumps({"Succcess": "User logged correctly"}),
                status=200,
                mimetype='application/json')
    else:
        return Response(response=json.dumps({"Error": "Something was wrong during login"}),
                        status=400,
                        mimetype='application/json')

@app.route('/profile')
def profile():
    if(currentUser.getEmail()):

        return render_template("profile.html",user=currentUser)
    else:
        return redirect('/')


@app.route('/delete')
def delete():
    if(currentUser.delete()):
        currentUser.disconnect()
        return redirect('/')
    else:
        return redirect('/profile')

@app.route('/showImage/<id>')
def show(id):
    if(currentUser.getEmail()):
        return render_template("showImage.html",myImage=myImages[int(id)].getImageBytes(),user=currentUser)
    else:
        return redirect('/')


@app.route('/images')
def images ():
    if currentUser.getEmail():
        #Usuario registrado o existe
        #Leo imágenes
        #imageRequest = requests.get('aux.TESTING_URL+readImages')
        imageRequest = requests.get(aux.DOCKER_URL+'readImages')
        if imageRequest.status_code == 200:
            data = json.loads(imageRequest.content)
            info = json_util.loads(data)
            index = 0
            myImages.clear()
            for i in info:
                
                myImages.append(aux.Image(index,i['imageName'],i['imageDate'],i['imageProcDate'],i['imageBytes']))
                  
                index= index+1
            #Pasar a lista la respuesta de mongo en b
            return render_template('images.html',images=myImages,user=currentUser)
        else:
            return redirect('/')
    else:
        return redirect('/')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001, debug=True)