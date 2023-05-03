from django.shortcuts import render
from django.http import HttpResponse
import requests


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
        if response.status_code==200:
            print("Correcto")
            return render(request, 'servicios.html',{'respuesta_servidor':'Aceptado'})
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