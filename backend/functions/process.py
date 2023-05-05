import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, ElementTree



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


def unificarDiccionarios(diccionario1, diccionario2):
    keys = set(diccionario1.keys()).union(set(diccionario2.keys()))
    nuevo_diccionario = {}
    for key in keys:
        valores1 = set(diccionario1.get(key, []))
        valores2 = set(diccionario2.get(key, []))
        nuevo_diccionario[key] = list(valores1.union(valores2))
    return nuevo_diccionario