from flask import Flask, render_template, redirect, request, Response
from pymongo import MongoClient
import jinja2
import requests
import json
import numpy as np
import certifi
from bson.objectid import ObjectId
from bson import json_util
import aux2 as aux
import base64
from datetime import date

app = Flask(__name__)

client = MongoClient("mongodb+srv://developers:devCloudDatabase@clusterhuntingtreasure.kux1l.mongodb.net/huntingtreasure?retryWrites=true&w=majority", tlsCAFile=certifi.where())
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
    if current_user.userEmail:
        #Juegos participando
        participando= juegosCollection.find( { "listaParticipantes":  { "$eq": current_user.userEmail } } )
        #Mostrar todos los juegos excepto los del user
        estado_juego="Activo"
        list_juegos = juegosCollection.find( { "creador": { "$ne" : current_user.userEmail }, "listaParticipantes": {"$nin": [current_user.userEmail]}  } )
        return render_template('juegos.html', list_participados=participando, estado=estado_juego,juegos=list_juegos,user=current_user, verTodos=True)
    else:
        return redirect("/")
@app.route("/misJuegos")
def myGames ():
    if current_user.userEmail:
        #Mostrar los juegos abiertos del usuario
        list_juegos = juegosCollection.find({"creador": { "$eq" :current_user.userEmail}})
        estado_juego="activo"
        return render_template('juegos.html', list_participados={},estado=estado_juego,juegos=list_juegos,user=current_user,verTodos=False)
    else:
        return redirect("/")
# Detalles del juego
@app.route("/detalles")
def detalles ():
    if current_user.userEmail:
        id=request.values.get("_id")
        current_juego = json_util.dumps(list(juegosCollection.find({"_id":ObjectId(id)})))
        juego_json = json.loads(current_juego)
        listaTesoros = juego_json[0]['tesoros']
        comentarios = juego_json[0]['comentarios']
        print(juego_json[0]['comentarios'])
        return render_template('detalles.html', juego=juego_json, user=current_user, tesoro = listaTesoros, comentario = comentarios)
    else:
        return redirect("/")

# Inscripcion al juego
@app.route("/inscribir")
def details ():
    if current_user.userEmail:
        id=request.values.get("_id")
        #mongodb update
        juego = juegosCollection.find({"_id":ObjectId(id)})
        juegosCollection.update_one( {"_id": ObjectId(id) },{"$push": { "listaParticipantes" : current_user.userEmail}})
        return redirect("/juegos")
    else:
        return redirect("/")

# Crear un juego
@app.route("/crearjuego", methods=['GET','POST'])
def creacionjuego():
    if current_user.userEmail:
        return render_template('crearjuego.html',user=current_user)
    else:
        return redirect("/")
    

# Modificar un juego
@app.route("/modificarjuego")
def modificacionjuego():
    if current_user.userEmail:
        id=request.values.get("_id")
        current_juego = json_util.dumps(list(juegosCollection.find({"_id":ObjectId(id)})))
        juego_json = json.loads(current_juego)
        print(juego_json[0])
        return render_template('modificarjuego.html',user=current_user, juego=juego_json[0], longitud=len(juego_json[0]['tesoros']))
    else:
        return redirect("/")
   

# Registrar un tesoro
@app.route("/registrartesoro")
def regtesoro():
    if current_user.userEmail:
        id=request.values.get("_id")
        current_juego = json_util.dumps(list(juegosCollection.find({"_id":ObjectId(id)})))
        juego_json = json.loads(current_juego)
        listaTesoros = juego_json[0]['tesoros']
        """for i in listaTesoros:
                print(i['coordenadaX'])"""
        return render_template('registrartesoro.html',user=current_user, juego=juego_json[0])
    else:
        return redirect("/")

# Guardar un comentario
@app.route('/saveComentario', methods=['GET','POST'])
def writeComment():
    if current_user.userEmail:
        id=request.form["identificador"]
        current_juego = json_util.dumps(list(juegosCollection.find({"_id":ObjectId(id)})))
        juego_json = json.loads(current_juego)
        listaTesoros = juego_json[0]['tesoros']
        comentarios = juego_json[0]['comentarios']
        mensaje = request.form["inputComentario"]
        autor = current_user.getUserName()
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        comentario = {'autor': autor,'mensaje':mensaje, 'fecha': d1}
        print(juego_json)
        if mensaje:
            response = juegosCollection.update_one( {"_id": ObjectId(id) },{"$push": { "comentarios" : comentario}})
            if response:
                return redirect('detalles?_id='+id)
            else:
                return Response(response=json.dumps({"Error": "Something wrong during insertion"}),
                            status=400,
                            mimetype='application/json')
        else:
            return Response(response=json.dumps({"Error": "Some field is empty"}),
                            status=400,
                            mimetype='application/json')
    else:
        return redirect("/")
# Guardar un juego
@app.route('/saveGame', methods=['GET','POST'])
def writeGame():
    if current_user.userEmail:
        nombre = request.form["inputNombre"]
        descripcion = request.form['inputDescripcion']
        fechaInicio = request.form['inputFechaInicio']
        fechaFin =  request.form['inputFechaFin']
        centroX = request.form['inputCentroX']
        centroY = request.form['inputCentroY']
        alto = request.form['inputAlto']
        ancho = request.form['inputAncho']
        nTesoros = request.form['total_chq']
        descripcionpista = request.form['inputPista']
        creador = current_user.getEmail()
        list_juegos = juegosCollection.find()
        insercion = {'creador': creador,'nombre':nombre, 'descripcion': descripcion, 'fechaInicio': fechaInicio,
            'fechaFin': fechaFin,'centro': {'coordenadaX': centroX, 'coordenadaY': centroY}, 'alto': alto, 'ancho': ancho, 'tesoros': [],
            'descripcionpista':descripcionpista,'imagen':"", 'estado':"Activo", 'listaParticipantes': [], 'comentarios': []}

        if nombre and descripcion and fechaInicio and fechaFin and centroX and centroY and alto and ancho and descripcionpista:
            response = juegosCollection.insert_one(insercion)
            usersCollection.update_one( {"userEmail": creador}, 
                                        {"$push": {"juegosParticipados": insercion }} )
            for i in range(1, int(nTesoros)+1):
                coordenadaX = request.form['inputCoordenadaX'+str(i)]
                coordenadaY = request.form['inputCoordenadaY'+str(i)]
                juegosCollection.update_one( {"_id": response.inserted_id },
                                        {"$push":{"tesoros":{'coordenadaX':coordenadaX, 'coordenadaY': coordenadaY, 'encontrado': False}}})
            if response:
                return redirect('/juegos')
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
    else:
        return redirect("/")

# Modificar un juego
@app.route('/modifyGame', methods=['GET','POST'])
def modifyGame():
    if current_user.userEmail:
        id=request.form["identificador"]
        nombre = request.form["inputNombre"]
        descripcion = request.form['inputDescripcion']
        fechaInicio = request.form['inputFechaInicio']
        fechaFin =  request.form['inputFechaFin']
        centroX = request.form['inputCentroX']
        centroY = request.form['inputCentroY']
        alto = request.form['inputAlto']
        ancho = request.form['inputAncho']
        nTesoros = request.form['total_chq']
        descripcionpista = request.form['inputPista']
        creador = current_user.getEmail()
        list_juegos = juegosCollection.find()
        insercion = {'creador': creador,'nombre':nombre, 'descripcion': descripcion, 'fechaInicio': fechaInicio,
            'fechaFin': fechaFin,'centro': {'coordenadaX': centroX, 'coordenadaY': centroY}, 'alto': alto, 'ancho': ancho, 'tesoros': [],
            'descripcionpista':descripcionpista,'imagen':"", 'estado':"Activo"}

        if nombre and descripcion and fechaInicio and fechaFin and centroX and centroY and alto and ancho and descripcionpista:
            response = juegosCollection.update_one({"_id": ObjectId(id) }, {"$set": insercion})
            for i in range(1, int(nTesoros)+1):
                coordenadaX = request.form['inputCoordenadaX'+str(i)]
                coordenadaY = request.form['inputCoordenadaY'+str(i)]
                juegosCollection.update_one( {"_id": ObjectId(id) },
                                        {"$push":{"tesoros":{'coordenadaX':coordenadaX, 'coordenadaY': coordenadaY, 'encontrado': False}}})
            if response:
                return redirect('detalles?_id='+id)
            else:
                return Response(response=json.dumps({"Error": "Something wrong during insertion"}),
                            status=400,
                            mimetype='application/json')
        else:
            return Response(response=json.dumps({"Error": "Some field is empty"}),
                            status=400,
                            mimetype='application/json')
    else:
        return redirect("/")

# Resetear un juego
@app.route('/resetjuego', methods=['GET','POST'])
def resetGame():
    if current_user.userEmail:
        id=request.values.get("_id")
        juegosCollection.update_one({"_id":ObjectId(id)},{ "$set" :{"listaParticipantes":[]} })
        current_juego = json_util.dumps(list(juegosCollection.find({"_id":ObjectId(id)})))
        juego_json = json.loads(current_juego)
        response = juegosCollection.update_one( {"_id": ObjectId(id) },{"$set": { "comentarios" : [],
                                                                            "tesoros.$[].encontrado" : False,
                                                                        "tesoros.$[].localizadoPor" : ""}})
    return redirect('detalles?_id='+id)


# Borrar un juego
@app.route('/borrarjuego', methods=['GET','POST'])
def deleteGame():
    if current_user.userEmail:
        id=request.values.get("_id")
        response = juegosCollection.delete_one( {"_id": ObjectId(id) })
    return redirect('/juegos')

# Registrar un tesoro
@app.route('/saveTreasure', methods=['GET','POST'])
def writeTreasure():
    if current_user.userEmail:
        id=request.form["identificador"]
        coordenadax = request.form['inputCoordenadaX1']
        coordenaday = request.form['inputCoordenadaY1']
        current_juego = json_util.dumps(list(juegosCollection.find({"_id":ObjectId(id)})))
        juego_json = json.loads(current_juego)
        nombre = current_user.getUserName()
        listaTesoros = juego_json[0]['tesoros']
        print(len(listaTesoros))
        contador = 0
        if coordenadax and coordenaday:
            for i in listaTesoros:
                if i['coordenadaX']==coordenadax and i['coordenadaY']==coordenaday:
                    if not(i['encontrado']):
                        juegosCollection.update_one( {"_id": ObjectId(id), "tesoros.coordenadaX": i['coordenadaX'], "tesoros.coordenadaY": i['coordenadaY']},
                                                            {"$set": {"tesoros.$.encontrado" : True}})
                        juegosCollection.update_one( {"_id": ObjectId(id), "tesoros.coordenadaX": i['coordenadaX'], "tesoros.coordenadaY": i['coordenadaY']},
                                                            {"$set": {"tesoros.$.localizadoPor" : nombre}})                                                        
                        break
                    else:
                        break
                contador += 1
            return redirect('detalles?_id='+id)
        else:
            return Response(response=json.dumps({"Error": "Some field is empty"}),
                            status=400,
                            mimetype='application/json')
    else:
        return redirect("/")
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
    if current_user.userEmail:
        current_user.disconnect()
        return redirect('/')
    else:
        return redirect("/")

@app.route('/delete')
def delete():
    email = current_user.userEmail
    if email:
        response = juegosCollection.delete_many({'creador': email})
        juegosCollection.update_many({ "listaParticipantes":  { "$eq": email } }
        , { "$pull": {"listaParticipantes": email} } )
        response = usersCollection.delete_one({'userEmail': email})
        if response:
            current_user.disconnect()
            return redirect('/')
        else:
            return redirect('/profile')
    else:
        return redirect ('/')


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
    #app.run(host="localhost", port=5000)
