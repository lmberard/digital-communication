"""
Codificacion de Huffman (Modulo B del enunciado).

Huffman es un metodo para convertir un texto en una tira de 0s y 1s lo
mas corta posible: a los caracteres que aparecen mas seguido les asigna
un codigo mas corto, y a los que aparecen poco, uno mas largo.

Las funciones de aca abajo todavia dicen "raise NotImplementedError", que
en criollo significa "esto todavia no esta hecho". Hay que ir
reemplazando eso, funcion por funcion, por el codigo real. No hace falta
hacerlas todas de una: se puede probar cada una por separado antes de
pasar a la siguiente.
"""


def analyze_text(file_path):
    """
    Lee el archivo de texto y calcula la probabilidad de aparicion de
    cada caracter (que porcentaje del texto ocupa cada uno).

    Ejemplo: si el texto fuera "aab", el resultado tendria que ser algo
    como {'a': 0.66, 'b': 0.33} (2 de cada 3 caracteres son 'a').

    Recibe:
        file_path -- la ruta del archivo de texto, por ejemplo
                      "data/example_text.txt"
    Devuelve:
        un diccionario {caracter: probabilidad}
    """
    raise NotImplementedError


def calculate_entropy(probabilities):
    """
    Calcula la entropia del texto: un numero que dice, en promedio,
    cuantos bits hacen falta como minimo para representar cada caracter.

    Recibe:
        probabilities -- el diccionario {caracter: probabilidad} que
                          devuelve analyze_text
    Devuelve:
        un numero (la entropia, en bits)
    """
    raise NotImplementedError


def generate_huffman_code(probabilities):
    """
    Arma el "diccionario de codigos" de Huffman: a cada caracter le
    asigna una palabra hecha de 0s y 1s. Los caracteres mas frecuentes
    tendrian que quedar con codigos mas cortos.

    Recibe:
        probabilities -- el diccionario {caracter: probabilidad}
    Devuelve:
        un diccionario {caracter: codigo}, donde el codigo es un texto
        de '0's y '1's, por ejemplo {'a': '0', 'b': '10', 'c': '11'}
    """
    raise NotImplementedError


def calculate_lengths(code, probabilities):
    """
    Calcula que tan bueno es el codigo que armamos: la longitud minima
    posible (segun la entropia), el promedio real de longitud de las
    palabras de codigo, y la varianza.

    Recibe:
        code -- el diccionario {caracter: codigo} de generate_huffman_code
        probabilities -- el diccionario {caracter: probabilidad}
    Devuelve:
        un diccionario con las claves 'min_length', 'avg_length' y
        'variance'
    """
    raise NotImplementedError


def encode_text(text, code):
    """
    Convierte el texto completo en una tira de 0s y 1s, reemplazando
    cada caracter por su codigo.

    Ejemplo: si code = {'a': '0', 'b': '10'} y text = "aab", el
    resultado tendria que ser "0010" (0 + 0 + 10).

    Recibe:
        text -- el texto original, tal cual se leyo del archivo
        code -- el diccionario {caracter: codigo}
    Devuelve:
        un texto hecho solo de '0's y '1's
    """
    raise NotImplementedError


def decode_bits(bits, code):
    """
    Hace lo inverso de encode_text: a partir de la tira de 0s y 1s,
    reconstruye el texto original usando el mismo diccionario de
    codigos.

    Recibe:
        bits -- el texto de '0's y '1's que devolvio encode_text
        code -- el mismo diccionario {caracter: codigo} que se uso
                para codificar
    Devuelve:
        el texto reconstruido
    """
    raise NotImplementedError


def save_text(text, output_path):
    """
    Guarda un texto en un archivo .txt.

    Recibe:
        text -- el texto a guardar
        output_path -- donde guardarlo, por ejemplo
                        "results/run1_received.txt"
    No devuelve nada, solo crea el archivo.
    """
    raise NotImplementedError
