from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from lxml import etree
from django.http import FileResponse
import os
import json
import requests
import xml.etree.ElementTree as ET


def index(request):
    title="Bienvenido a la aplicación del proyecto 3!"
    return render (request, "index.html", {
        "title": title,
    })

def hello(request):
    return  HttpResponse("<h2>Hello </h2>")

def servicios(request):
    if request.method=="POST":
        archivo=request.FILES['archivo']
        headers = {"Content-Type": "application/xml"}
        response = requests.post('http://127.0.0.1:5000/cargarPerfiles', data=archivo.read(), headers=headers)
        contadorMensaje=0
        valorUsuarios=0
        if response.status_code==200:
            print("Correcto")

            respuesta = response.json()
            try:
                contadorMensaje=respuesta["contadorMensaje"]
                valorUsuarios=respuesta["usuariosDistintos"]
            except:
                pass

            print(contadorMensaje)
            print(valorUsuarios)
            if contadorMensaje !=0 or valorUsuarios !=0:
                # Crear la estructura XML
                root = ET.Element("respuesta")
                usuarios = ET.SubElement(root, "usuarios")
                usuarios.text = f"Se procesaron mensajes para {valorUsuarios} usuarios distintos"
                mensajes = ET.SubElement(root, "mensajes")
                mensajes.text = f"Se procesaron {contadorMensaje} mensajes en total"
                respuesta_xml = ET.tostring(root, encoding="unicode")

                return render(request, 'servicios.html',{'xml_respuesta': respuesta_xml})
            else:
                # Convertir respuesta JSON a XML
                root = ET.Element("respuesta")
                perfiles_nuevos = ET.SubElement(root, "perfilesNuevos")
                perfiles_nuevos.text = str(respuesta["perfilesNuevos"])
                perfiles_modificados = ET.SubElement(root, "perfilesModificados")
                perfiles_modificados.text = str(respuesta["perfilesModificados"])
                descartadas_agregadas = ET.SubElement(root, "descartadasAgregadas")
                descartadas_agregadas.text = str(respuesta["descartadasAgregadas"])

                xml_respuesta = ET.tostring(root, encoding="unicode")
                return render(request, 'servicios.html', {'xml_respuesta': xml_respuesta})
        else:
            print("incorrecto")
            return render(request, 'servicios.html',{'respuesta_servidor':'Incorrecto'})
    else:
        return render(request, 'servicios.html',{'respuesta_servidor':''})

def peticiones(request):
    return render(request, 'peticiones.html')

def ayuda(request):
    return render(request, 'ayuda.html')

def reset(request):
    
    if request.method == 'POST':
        # Definir los parámetros de la solicitud
        headers = {'Content-Type': 'application/json'}
        data = {'reset': True}

        # Enviar la solicitud POST a la API
        response = requests.post('http://127.0.0.1:5000/resetDatos', headers=headers, data=json.dumps(data))

        # Manejar la respuesta de la API
        if response.status_code == 200:
            return render(request, 'reset.html', {'respuesta': 'Se ha reiniciado la base de datos.'})
        else:
            return render(request, 'reset.html', {'respuesta': 'No se ha podido reiniciar la base de datos.'})
    else:
        return render(request, 'reset.html', {'respuesta': ''})

#peticioneeeeeees
def detalle_mensajes(request):
    # Código para obtener y procesar la información de mensajes por usuario
    
    if request.method == 'POST':
        # Recuperar los datos del formulario y cambiando el formato de fecha
        fecha = request.POST.get('fecha')
        fecha2 = request.POST.get('fecha2')
        fecha_str = datetime.strptime(fecha, "%Y-%m-%d")
        fecha2_str = datetime.strptime(fecha2, "%Y-%m-%d")
        fecha_formato = fecha_str.strftime("%d/%m/%Y")
        fecha2_formato = fecha2_str.strftime("%d/%m/%Y")

        usuario = request.POST.get('usuario')
        print(fecha_formato)
        print(fecha2_formato)
        print(usuario)
        data = {'fecha': fecha_formato, 'fecha2': fecha2_formato, 'usuario': usuario}
        #Enviar la solicitud al servidor
        response=requests.post('http://127.0.0.1:5000/consultarFecha', data=data)
        
    informacion = "hola"
    return render(request, 'peticiones.html', {'informacion': informacion})

def resumen_pesos(request):
    # Código para obtener y procesar la información de pesos por usuario
    if request.method == 'POST':
        headers = {'Content-Type': 'application/json'}
        # Recuperar los datos del formulario
        usuario = request.POST.get('usuario')
        data={'usuario':usuario}
        #Enviar la solicitud al servidor
        response=requests.post('http://127.0.0.1:5000/consultarPesos', headers=headers, data=json.dumps(data))
        print(response)
    

    informacion = "hola"
    return render(request, 'peticiones.html', {'informacion': informacion})

def prueba_solicitudes(request):
    # Código para enviar una solicitud con un mensaje
    # ...
    informacion = "hola"
    return render(request, 'peticiones.html', {'informacion': informacion})

def abrir_pdf(request):
    filename = 'static/Ensayo_202010844.pdf'
    response = FileResponse(open(filename, 'rb'), content_type='application/pdf')
    return response