from flask import Flask,request,jsonify
from flask_debugtoolbar import DebugToolbarExtension
from functions.process import xmlADiccionario,EscribirBasePalabras,unificarDiccionarios,CargaMensajes
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
        contadorMensaje = 0
        usuarios_distintos = set()
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
            
            for mensaje in root.findall('.//mensaje'):

                lugar_y_fecha = mensaje.text.split('\n')[1].strip()
    
                # Dividir el texto en dos partes: lugar y fecha/hora
                fecha_hora = lugar_y_fecha.split(': ')[1]
                lugar=fecha_hora.split(', ')[0]
                fecha_hora=fecha_hora.split(', ')[1]
                fecha, hora = fecha_hora.split(' ')

                usuario = mensaje.text.split('\n')[2].strip().split(': ')[1]
                red_social = mensaje.text.split('\n')[3].strip().split(': ')[1]
                mensaje_texto = ' '.join(mensaje.text.split('\n')[4:]).strip()
                palabras = mensaje_texto.split()
                xml= f"<mensaje><lugar>{lugar}</lugar><fecha>{fecha}</fecha><hora>{hora}</hora><usuario>{usuario}</usuario><redSocial>{red_social}</redSocial><mensaje>{mensaje_texto}</mensaje><palabrasClave>{palabras}</palabrasClave></mensaje>"
                CargaMensajes(xml)
                usuarios_distintos.add(usuario)
                contadorMensaje += 1
                flag = True
            print(f"Se han cargado {contadorMensaje} mensajes de {len(usuarios_distintos)} usuarios distintos")
            #if flag:
            #    return jsonify({{contadorMensaje},{len(usuarios_distintos)}})
        else:
            respuesta=EscribirBasePalabras(xmlADiccionario(request.data))
        
        if flag:
                valorUsuarios = len(usuarios_distintos)
                return jsonify({"contadorMensaje": contadorMensaje, "usuariosDistintos": valorUsuarios})
        else:
            return jsonify(respuesta)
    else:
        return "Wrong response"
        
