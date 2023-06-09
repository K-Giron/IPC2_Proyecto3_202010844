import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, ElementTree
from flask import request, jsonify
from io import BytesIO
import os


def CargaMensajes(xml_string):

    if xml_string:
        doc=ET.fromstring(xml_string)
        lugar=doc.find("lugar").text
        fecha=doc.find("fecha").text
        hora=doc.find("hora").text
        usuario=doc.find("usuario").text
        red_social=doc.find("redSocial").text
        mensaje=doc.find("mensaje").text
        palabras_clave=doc.find("palabrasClave").text.split()

        #eliminar las palabras clave que estan en descartadas
        try:
            tree = ET.parse('diccionario.xml')
            root = tree.getroot()
        except FileNotFoundError:
            root = ET.Element('perfiles')
        for perfil in root.findall('perfil'):
            if perfil.find('nombre').text == "descartadas":
                palabras_descartadas = [p.text for p in perfil.findall('.//palabra')]
                break
        palabras_clave = [p for p in palabras_clave if p not in palabras_descartadas]


        root= ET.Element("mensajes")
        mensaje_element = ET.Element('mensaje')
        lugar_element = ET.SubElement(mensaje_element, 'lugar')
        lugar_element.text = lugar
        fecha_element = ET.SubElement(mensaje_element, 'fecha')
        fecha_element.text = fecha
        hora_element = ET.SubElement(mensaje_element, 'hora')
        hora_element.text = hora
        usuario_element = ET.SubElement(mensaje_element, 'usuario')
        usuario_element.text = usuario
        red_social_element = ET.SubElement(mensaje_element, 'redSocial')
        red_social_element.text = red_social
        mensaje_texto_element = ET.SubElement(mensaje_element, 'mensajeTexto')
        mensaje_texto_element.text = mensaje
        palabras_clave_element = ET.SubElement(mensaje_element, 'palabrasClave')
        for palabra in palabras_clave:
            palabra_element = ET.SubElement(palabras_clave_element, 'palabra')
            palabra_element.text = palabra
        
        # Abrimos el archivo mensajes.xml en modo "append"
        tree = ET.ElementTree()
        try:
            tree.parse('mensajes.xml') # Si el archivo ya existe, lo cargamos
            root = tree.getroot()
        except FileNotFoundError:
            # Si el archivo no existe, creamos la raíz del árbol
            root = ET.Element('mensajes')
            tree._setroot(root)

        # Añadimos el nuevo mensaje a la raíz
        root.append(mensaje_element)

        # Guardamos el archivo actualizado
        tree.write('mensajes.xml', encoding='utf-8', xml_declaration=True)



def EscribirBasePalabras(datos):
    # Cargamos el archivo XML actual
    try:
        tree = ET.parse('diccionario.xml')
        root = tree.getroot()
    except FileNotFoundError:
        root = ET.Element('perfiles')
    
    # Contadores para el resumen de cambios
    perfiles_nuevos = 0
    perfiles_actualizados = 0
    palabras_descartadas_agregadas = 0
    
    # Iteramos sobre cada perfil y agregamos sus palabras clave
    for key, value in datos.items():
        # Buscamos el perfil en el archivo XML
        perfil_existente = False
        for perfil in root.findall('perfil'):
            if perfil.find('nombre').text == key:
                perfil_existente = True
                # Si ya existe el perfil, actualizamos sus palabras clave
                palabras = perfil.find('palabrasClave')
                palabras_actualizadas = 0
                descartadas_actualizadas = 0
                for palabra in value:
                    if palabra not in [p.text for p in palabras.findall('palabra')]:
                        ET.SubElement(palabras, 'palabra').text = palabra
                        palabras_actualizadas += 1
                        if key == "descartadas":  # añadimos condición para descartadas
                            descartadas_actualizadas += 1
                if palabras_actualizadas > 0:
                    perfiles_actualizados += 1
                if descartadas_actualizadas > 0:  # añadimos condición para descartadas
                    palabras_descartadas_agregadas += descartadas_actualizadas
                break
        
        # Si el perfil no existe, lo creamos
        if not perfil_existente:
            head = ET.SubElement(root,'perfil')
            ET.SubElement(head, 'nombre').text = key
            elemento = ET.SubElement(head,'palabrasClave')
            for item in value:
                ET.SubElement(elemento, 'palabra').text = item
            perfiles_nuevos += 1
            if key == "descartadas":
                palabras_descartadas_agregadas += len(value)
        
    
    # Creamos el elemento XML de respuesta
    respuesta = {
        'perfilesNuevos': perfiles_nuevos,
        'perfilesModificados': perfiles_actualizados,
        'descartadasAgregadas': palabras_descartadas_agregadas
    }
    
    # Escribimos los cambios al archivo XML
    tree = ET.ElementTree(root)
    tree.write('diccionario.xml', encoding='utf-8', xml_declaration=True)
    
    
    
    # Retornamos la respuesta
    return respuesta
    


def xmlADiccionario(xml_string):
    root = ET.fromstring(xml_string)
    result_dict = {}
    for perfil in root.findall('.//perfil'):
        nombre = perfil.find('nombre').text
        palabras = [p.text for p in perfil.findall('.//palabra')]
        result_dict[nombre] = palabras

    for descartadas in root.findall('.//descartadas'):
        palabras = [p.text for p in descartadas.findall('.//palabra')]
        result_dict['descartadas'] = palabras

    return result_dict

def xmlADiccionarioMensajes(xml_string):
    root = ET.fromstring(xml_string)
    result_dict = {}
    mensajes= root.findall('mensaje')
    print(mensajes)
    for i, mensaje in enumerate(mensajes):
        lugar = mensaje.find('lugar').text
        fecha = mensaje.find('fecha').text
        hora = mensaje.find('hora').text
        usuario = mensaje.find('usuario').text
        red_social = mensaje.find('redSocial').text
        mensaje_texto = mensaje.find('mensajeTexto').text
        palabras_clave = [p.text for p in mensaje.findall('.//palabra')]
        result_dict[f'mensaje_{i+1}'] = {
            'lugar': lugar,
            'fecha': fecha,
            'hora': hora,
            'usuario': usuario,
            'redSocial': red_social,
            'mensaje': mensaje_texto,
            'palabrasClave': palabras_clave
        }
    
    return result_dict


def unificarDiccionarios(diccionario1, diccionario2):
    keys = set(diccionario1.keys()).union(set(diccionario2.keys()))
    nuevo_diccionario = {}
    for key in keys:
        valores1 = set(diccionario1.get(key, []))
        valores2 = set(diccionario2.get(key, []))
        nuevo_diccionario[key] = list(valores1.union(valores2))
    return nuevo_diccionario

def ProcessPesos(usuario):
    pass