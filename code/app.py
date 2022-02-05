from flask import Flask, render_template, redirect, request, Response
from pymongo import MongoClient
import jinja2
import requests
import json
import numpy as np
from cv2 import cv2
from bson import json_util
import aux2 as aux
import base64

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
proyectoDB = client['Proyecto']
juegosCollection = proyectoDB['juegos']
usersCollection = proyectoDB['usuarios']

current_user = aux.User("","",False,[],[])

@app.route('/')
def index():
    return render_template("index.html")

# Pagina principal con todos los juegos
@app.route("/juegos")
def games ():
    #Juegos participando
    participando= juegosCollection.find({ })
	#Mostrar todos los juegos excepto los del user
    list_juegos = juegosCollection.find( { "creador": { "$ne" : current_user.userEmail } })
    return render_template('juegos.html',juegos=list_juegos,user=current_user)

"""
@app.route("/misJuegos")
def myGames ():
	#Mostrar los juegos abiertos del usuario
    userEmail = current_user.getEmail()
	list_juegos = juegosCollection.find({"creador":userEmail})
	estado_juego="activo"
	return render_template('juegos.html',estado=estado_juego,juegos=list_juegos)
"""


# Detalles del juego
@app.route("/detalles")
def detalles ():
    id=request.values.get("_id")
    current_juego = juegos.find({"_id":ObjectId(id)})
    return render_template('detalles.html',juego=current_juego) # Aun no existe

# Inscripcion al juego
@app.route("/inscribir", methods=['POST'])
def details ():
    id=request.values.get("_id")
    #mongodb update
    return render_template('inscribir.html',juego=current_juego)

# Crear un juego
@app.route("/crearjuego", methods=['GET','POST'])
def creacionjuego():
    return render_template('crearjuego.html')

# Guardar un juego
@app.route('/saveGame', methods=['GET','POST'])
def writeGame():
    nombre = request.form["inputNombre"]
    descripcion = request.form['inputDescripcion']
    fechaInicio = request.form['inputFechaInicio']
    fechaFin =  request.form['inputFechaFin']
    centro = request.form['inputCentro']
    alto = request.form['inputAlto']
    ancho = request.form['inputAncho']
    coordenadaX = request.form['inputCoordenadaX']
    coordenadaY =request.form['inputCoordenadaY']
    descripcionpista = request.form['inputPista']
    imagen = request.form['inputImagen']
    creador = current_user.getEmail()
    list_juegos = juegosCollection.find()
    insercion = {'creador': creador,'nombre':nombre, 'descripcion': descripcion, 'fechaInicio': fechaInicio,
         'fechaFin': fechaFin,'centro':centro, 'alto': alto, 'ancho': ancho,'coordenadaX':coordenadaX, 'coordenadaY': coordenadaY,
         'descripcionpista':descripcionpista,'imagen':imagen, 'estado':"Activo"}

    if nombre and descripcion and fechaInicio and fechaFin and centro and alto and ancho and coordenadaX and coordenadaY and descripcionpista and imagen:
        response = juegosCollection.insert_one(insercion)
        usersCollection.update_one( {"userEmail": creador}, 
                                    {"$push": {"juegosParticipados": insercion }} )
        if response:
            return render_template('juegos.html',juegos=list_juegos,user=current_user)
            """Response(response=json.dumps({"Message": "Correct insertion"}),
                        status=200,
                        mimetype='application/json')"""
        else:
            return Response(response=json.dumps({"Error": "Something wrong during insertion"}),
                        status=400,
                        mimetype='application/json')
    else:
        return Response(response=json.dumps({"Error": "Some field is empty"}),
                        status=400,
                        mimetype='application/json')


#-------------User Control----------------------#
#Login
@app.route('/login', methods=['POST'])
def login():
    #recibir datos de google oauth
    userEmail = request.form["userEmail"]
    userName = request.form["userName"]
    if userName and userEmail:
        results = usersCollection.count_documents({'userEmail': userEmail})
        if results <=0:
            response = usersCollection.insert_one({'userName':userName, 'userEmail': userEmail, 'isAdmin': False, 'juegosParticipados': []})
            if response:
                current_user.setEmail(userEmail)
                current_user.setUserName(userName)
                current_user.setIsAdmin(False)
                current_user.setJuegosParticipados([])
                return Response(response=json.dumps({"Message": "Correct insertion"}),
                            status=200,
                            mimetype='application/json')
            else:
                return Response(response=json.dumps({"Error": "Something was wrong during insertion"}),
                            status=400,
                            mimetype='application/json')
        else:
            usuarios = usersCollection.find({'userEmail': userEmail})
            user = usuarios[0]
            current_user.setEmail(user["userEmail"])
            current_user.setUserName(user["userName"])
            current_user.setIsAdmin(user["isAdmin"])
            current_user.setJuegosParticipados(user["juegosParticipados"])
            mygames = juegosCollection.find({'creator': user["userEmail"]})
            current_user.setMisJuegos(mygames)
            return Response(response=json.dumps({"Message": "User is already registered"}),
                            status=200,
                            mimetype='application/json')
    else:
        return Response(response=json.dumps({"Error": "Some field is empty"}),
                        status=400,
                        mimetype='application/json')

#LOGOUT
@app.route('/logout')
def logout():
    current_user.disconnect()
    return redirect('/')

@app.route('/delete')
def delete():
    #Falta eliminar los juegos creados por este usuario y eliminar su participación
    email = request.form['userEmail']
    if email:
        response = current_user.delete_one({'userEmail': email})
        if response:
            currentUser.disconnect()
            return redirect('/')
        else:
            return redirect('/profile')
    else:
        return Response(response=json.dumps({"Error": "Some field is empty"}),
                        status=400,
                        mimetype='application/json')

#Datos del Perfil
@app.route('/perfil')
def profile():
    if(current_user.getEmail()):
        usuarios = usersCollection.find({'userEmail': current_user.getEmail()})
        user = usuarios[0]
        current_user.setEmail(user["userEmail"])
        current_user.setUserName(user["userName"])
        current_user.setIsAdmin(user["isAdmin"])
        current_user.setJuegosParticipados(user["juegosParticipados"])
        mygames = juegosCollection.find({'creador': user["userEmail"]})
        current_user.setMisJuegos(mygames)
        return render_template("profile.html",user=current_user)
    else:
        return redirect('/')

#-------------User Control----------------------#
        
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=6001, debug=True)