import json, flask
from flask import Flask, jsonify, Response, request
from http import HTTPStatus
import requests
import threading

app = Flask(__name__)

with open("biblioteca.json",encoding='utf-8') as biblioteca_json:
    peliculas=json.load(biblioteca_json) 
peliculas=peliculas[0]['peliculas']

with open("usuarios.json",encoding='utf-8') as usuarios_json:
    usuarios=json.load(usuarios_json)
usuarios=usuarios[0]['usuarios']

with open("directores.json",encoding='utf-8') as directores_json:
    directores=json.load(directores_json)
directores=directores[0]['directores']

with open("actores.json",encoding="utf-8") as actores_json:
    actores=json.load(actores_json)
actores=actores[0]['actores']

print("Bienvenido a Stremio!\n")

ultimas_peliculas_agregadas=[]
@app.route("/")     # Muestra las ultimas 10 peliculas agregadas
def home():
    if len(ultimas_peliculas_agregadas)>0:
        return jsonify(ultimas_peliculas_agregadas)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)


@app.route("/usuarios")     # Muestra todos los usuarios
def devolver_usuarios():
    lista=[]
    for usuario in usuarios:
        lista.append(usuario['usuario'])
    if len(lista)>0:
        return jsonify(lista)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)


@app.route("/peliculas")   #    Muestra todas las peliculas
def devolver_peliculas():
    mostrar_peliculas=[]
    for pelicula in peliculas:
        mostrar_peliculas.append(pelicula['titulo'])
    if len(mostrar_peliculas)>0:
        return jsonify(mostrar_peliculas)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)    


@app.route("/peliculas/<id>")   # Muestra las peliculas por id 
def devolver_pelicula(id):
    id_int=int(id)
    for pelicula in peliculas:
        if pelicula['id']==id_int:
            return jsonify(pelicula)
    return Response("No encontrado", status=HTTPStatus.NOT_FOUND)


@app.route("/directores")   # Muestra todos los directores
def directores_imprimir():
    lista=[]
    for pelicula in peliculas:
        if pelicula['director'] not in lista:
            lista.append(pelicula['director'])
    if len(lista)>0:
        return jsonify(lista)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)


@app.route("/generos")      # Muestra todos los generos
def generos_imprimir():
    lista=[]
    for pelicula in peliculas:
        if pelicula['genero'] not in lista:
            lista.append(pelicula['genero'])
    if len(lista)>0:
        return jsonify(lista)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)


@app.route("/peliculas/imagen")     # Muestra las peliculas que tienen imagen
def devolver_peliculas_con_imagen():
    dic={}
    for pelicula in peliculas: 
        if "link" in pelicula:
            dic[pelicula['titulo']]=pelicula['link']
    if len(dic)>0:
        return jsonify(dic)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)
    

@app.route("/directores/<id>")      # Muestra todas las peliculas cargadas de un director especifico por id  
def devolver_peliculas_director(id):
    id_int=int(id)
    lista=[]
    for director in directores:
        if id_int==director['id']:
            variable=director['director']
    for pelicula in peliculas:
        if pelicula['director']==variable:
            lista.append(pelicula['titulo'])
    if len(lista)>0:
        return jsonify(lista)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)

@app.route("/actores/<id>")
def devolver_peliculas_actores(id): # Muestra todas las peliculas cargadas por actor especifico via id
    id_int=int(id)
    lista=[]
    for actor in actores:
        if id_int==actor['id']:
            variable_actor=actor['actor']
    for pelicula in peliculas:
        if pelicula['actor']==variable_actor:
            lista.append(pelicula['titulo'])
    if len(lista)>0:
        return jsonify(lista)
    else:
        return Response("No encontrado", status=HTTPStatus.NOT_FOUND)       


@app.route("/peliculas/eliminar/<int:id>",methods=["DELETE"])      # Elimina una pelicula por id 
def eliminar_pelicula(id):
    id_int=int(id)
    valor=False
    for pelicula in peliculas:
        if pelicula['id']==id_int:
            peliculas.remove(pelicula)
            valor=True
    if valor==True:
        return Response("Eliminado",status=HTTPStatus.OK)
    else:  
        return Response("Solicitud incorrecta",status=HTTPStatus.BAD_REQUEST)


@app.route("/peliculas/publicar", methods=["POST"])     # Publica nueva pelicula 
def comprar_entrada():                                  
    datos=request.get_json()                            

    for director in directores:         # Si es un director nuevo lo agrega a directores.json
        id=director['id']
    id+=1
    if datos['director'] not in directores:     
        directores.append({
            "id":id,
            "director":datos['director']
            })
        
    if len(ultimas_peliculas_agregadas)<10:                 # Agrega las ultimas 10 peliculas a la pagina home
        ultimas_peliculas_agregadas.append(datos['titulo'])     
    else:
        for i in range(9,-1,-1):
            if i != 0:
                ultimas_peliculas_agregadas[i]=ultimas_peliculas_agregadas[i-1]
            ultimas_peliculas_agregadas[0]=datos['titulo'] 

    if (datos['id'] not in peliculas):      # Post
        peliculas.append(datos)
      
        return Response("OK",status=HTTPStatus.OK)
    else:
        return Response("Solicitud incorrecta",status=HTTPStatus.BAD_REQUEST)


@app.route("/peliculas/actualizar", methods=["PUT"])    # Modifica pelicula especifica segun id 
def modificar_pelicula():
    datos=request.get_json()
    if "id" in datos:
        for pelicula in peliculas:
            if(datos['id']==pelicula['id']):
                if "titulo" in datos:
                    pelicula['titulo']=datos["titulo"]
                if "anio" in datos:
                    pelicula['anio']=datos["anio"]
                if "director" in datos:
                    pelicula['director']=datos["director"]
                    if datos['director'] not in directores:
                        for director in directores:
                            id=director['id']
                            id+=1
                        directores.append({
                            "id":id,
                            "director":datos['director']
                        })
                if "genero" in datos:
                    pelicula['genero']=datos["genero"]
                if "sinopsis" in datos:
                    pelicula['sinopsis']=datos["sinopsis"]
                if "link" in datos:
                    pelicula['link']=datos["link"]          
                return Response("OK",status=HTTPStatus.OK)
    else:
        return Response("ID no encontrado",status=HTTPStatus.NOT_FOUND)


login=False
def menu():
    print("")
    while True:
        print("           MENU             ")
        print("----------------------------")
        print("0: Iniciar/cerrar sesion")
        print("1: Mostrar todas las peliculas")
        print("2: Mostrar pelicula especifica")
        print("3: Mostrar ultimas peliculas agregadas")
        print("4: Mostrar peliculas con imagenes")
        print("5: Mostrar directores")
        print("6: Mostrar peliculas de un director especifico")
        print("7: Mostrar peliculas de un actor especifico")
        print("8: Mostrar usuarios")
        print("9: Mostrar generos")
        print("10: Eliminar pelicula")
        print("11: Publicar pelicula")
        print("12: Modificar pelicula")
        print("13: Salir")
        opcion=int(input("Ingresar opcion: "))
        print("")

        if (opcion==0):
            global login
            if(login==False):
                user=input("Ingresar usuario: ")
                password=input('Ingresar contraseña: ')
                for usuario in usuarios:
                    if(user in usuario['usuario'] and password in usuario['contrasenia']):
                        login=True
                if (login==True):
                    print("Inicio de sesion exitoso")
                else:
                    print("Error al iniciar sesion")
            else:
                login=False
                print("Sesion cerrada")

        elif (opcion==1):
            r=(requests.get("http://127.0.0.1:5000/peliculas"))
            r=r.json()
            for i in r:
                print(i)

        elif (opcion==2):   
            id=input("Ingresar id de la pelicula: ")
            r=(requests.get("http://127.0.0.1:5000/peliculas/"+id))
            r=r.json()
            for key,value in r.items():
                print(key," : ",value)

        elif (opcion==3):
            r=(requests.get("http://127.0.0.1:5000"))
            r=r.json()
            for i in r:
                print(i)

        elif (opcion==4):
            r=(requests.get("http://127.0.0.1:5000/peliculas/imagen"))
            r=r.json()
            for key,value in r.items():
                print(key," : ",value)

        elif (opcion==5):
            r=(requests.get("http://127.0.0.1:5000/directores"))
            r=r.json()
            for i in r:
                print(i)

        elif (opcion==6): 
            id=input("Ingresar id del director: ")
            r=(requests.get("http://127.0.0.1:5000/directores/"+id))
            r=r.json()
            for i in r:
                print(i)

        elif(opcion==7):
            id=input("Ingrese ID del Actor")
            r=(requests.get("http://127.0.0.1:5000/actores/"+id))
            r=r.json()
            for i in r:
                print(i)

        elif (opcion==8):
            r=(requests.get("http://127.0.0.1:5000/usuarios"))
            r=r.json()
            for i in r:
                print(i)

        elif (opcion==9):
            r=(requests.get("http://127.0.0.1:5000/generos"))
            r=r.json()
            for i in r:
                print(i)

        elif (opcion==10):
            if(login==False):
                print("Permiso denegado, inicie sesion.")
            else:
                id=input("Ingresar id de la pelicula: ")
                r=(requests.delete("http://127.0.0.1:5000/peliculas/eliminar/"+id))
                print(r.content)

        elif (opcion==11):
            if(login==False):
                print("Permiso denegado, inicie sesion.")
            else:
                id=int(input("Ingresar id: "))
                titulo=input("Titulo: ")
                anio=input("Año: ")
                director=input("Director: ")
                genero=input("Genero: ")
                sinopsis=input("Sinopsis: ")
                link=input("Link imagen/portada: ")
                j={
                    "id":id,
                    "titulo":titulo,
                    "anio":anio,
                    "director":director,
                    "genero":genero,
                    "sinopsis":sinopsis,
                    "link":link
                }
                r=(requests.post("http://127.0.0.1:5000/peliculas/publicar",json=j))
                print(r.content)

        elif (opcion==12):
            if(login==False):
                print("Permiso denegado, inicie sesion.")
            else:
                id=int(input("Ingresar id de la pelicula: "))
                valor=False
                for pelicula in peliculas:
                    if id==pelicula['id']:
                        valor=True
                        dic_pelicula=pelicula
                if valor==False:
                    print("ID no encontrado")
                else:
                    respuesta=input("¿Modificar el titulo?")
                    if(respuesta=='si' or respuesta=='SI'):
                        titulo=input("Ingresar titulo: ")
                    else:
                        titulo=dic_pelicula['titulo']
                    respuesta=input("¿Modificar el año?")
                    if(respuesta=='si' or respuesta=='SI'):
                        anio=input("Ingresar año: ")
                    else:
                        anio=dic_pelicula['anio']
                    respuesta=input("¿Modificar el director?")
                    if(respuesta=='si' or respuesta=='SI'):
                        director=input("Ingresar director: ")
                    else:
                        director=dic_pelicula['director']
                    respuesta=input("¿Modificar el genero?")
                    if(respuesta=='si' or respuesta=='SI'):
                        genero=input("Ingresar genero: ")
                    else:
                        genero=dic_pelicula['genero']
                    respuesta=input("¿Modificar la sinopsis?")
                    if(respuesta=='si' or respuesta=='SI'):
                        sinopsis=input("Ingresar sinopsis: ")
                    else:
                        sinopsis=dic_pelicula['sinopsis']
                    respuesta=input("¿Modificar el link de la imagen?")
                    if(respuesta=='si' or respuesta=='SI'):
                        link=input("Ingresar link: ")
                    else:
                        link=dic_pelicula['link']
                    j={
                        "id":id,
                        "titulo":titulo,
                        "anio":anio,
                        "director":director,
                        "genero":genero,
                        "sinopsis":sinopsis,
                        "link":link
                    }
                    r=(requests.put("http://127.0.0.1:5000/peliculas/actualizar",json=j))
                    print(r.content)

        elif (opcion==13):
            print("Exit!\n")
            exit()

        else:
            print("Error al ingresar opcion")
        print("")

m = threading.Timer(1,menu)
m.start()
if __name__ == '__main__':
    app.run(port=5000)