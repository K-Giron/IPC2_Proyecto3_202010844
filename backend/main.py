from flask import Flask,request,jsonify
from flask_debugtoolbar import DebugToolbarExtension
from functions.process import xmlADiccionario,EscribirBasePalabras,unificarDiccionarios
import xml.etree.ElementTree as ET
import os


app = Flask(__name__)
app.debug=True 
print("Iniciando el servidor en el puerto por defecto (5000)")

@app.route("/")
def hello_world():
    return jsonify({"MSG":"Hola a todos esto es parte de flask"})

@app.route("/UsuarioConectado",methods=["GET"])
def UsuarioConectado():
    nombreUser= request.args.get("nombreUser")
    print(nombreUser)
    return jsonify({"Nombre":nombreUser})

@app.route("/ObtenerDatos",methods=["POST"])
def ObtenerDatos():
    perfil = request.get_json()
    print(perfil)
    if(perfil["id"]==1):
        return jsonify({"MSG":"Usuario bloqueado, Jorge debe dinero"})
    return jsonify({"MSG":"Usuario autorizado"})

@app.route("/cargarPerfiles",methods=['POST'])
def Cargar():
    if request.method=='POST':
        flag = False
        ruta_archivo = 'diccionario.xml'
        if os.path.exists(ruta_archivo):
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()
            xml_string = ET.tostring(root, encoding='utf8', method='xml').decode('utf8')
            diccionario1=xmlADiccionario(request.data)
            diccionario2=xmlADiccionario(xml_string)
            diccionarioNuevo=unificarDiccionarios(diccionario1,diccionario2)
            respuesta=EscribirBasePalabras(diccionarioNuevo)
            #print(respuesta)
#------------------------------------------------------------------------------------esto sigue mal
            # Analizar el archivo XML de lista de mensajes
            root = ET.fromstring(request.data)
            print(root)
            for mensaje in root.findall('.//mensaje'):
                print(mensaje.text)
                # Obtener el texto completo de la etiqueta "Lugar y Fecha"
                lugar_y_fecha = mensaje.text.split('\n')[1].strip()
                
                # Dividir el texto en dos partes: lugar y fecha/hora
                lugar, fecha_hora = lugar_y_fecha.split(': ')
                fecha, hora = fecha_hora.split(' ')

                usuario = mensaje.text.split('\n')[2].strip().split(': ')[1]
                red_social = mensaje.text.split('\n')[3].strip().split(': ')[1]
                mensaje_texto = ' '.join(mensaje.text.split('\n')[4:]).strip()
                palabras = mensaje_texto.split()

                print('Lugar:', lugar)
                print('Fecha:', fecha)
                print('Hora:', hora)
                print("Usuario: ", usuario)
                print("Red social: ", red_social)
                print("Mensaje: ", mensaje_texto)
                print("Palabras: ", palabras)
                flag = True
        else:
            
            respuesta=EscribirBasePalabras(xmlADiccionario(request.data))
            print(respuesta)
        #if flag:
            #return jsonify(respuesta)
        return jsonify(respuesta)



    else:
        return "Wrong response"
        
