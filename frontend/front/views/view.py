from django.shortcuts import render
from django.http import HttpResponse
from lxml import etree
import requests
import xml.etree.ElementTree as ET


def index(request):
    title="Welcome to Django Course!!"
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
    return render(request, 'reset.html')