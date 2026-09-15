"""
Codificacion de Huffman (Modulo B del enunciado). Ya esta completo.

Huffman es un metodo para convertir un texto en una tira de 0s y 1s lo
mas corta posible: a los caracteres que aparecen mas seguido les asigna
un codigo mas corto, y a los que aparecen poco, uno mas largo.

Las funciones de "Transmisor" (analyze_text, calculate_entropy,
generate_huffman_code, calculate_lengths, encode_text) arman el codigo y
codifican el texto. Las de "Receptor" (decode_bits, save_text) hacen el
camino inverso. is_prefix_code es un chequeo extra que pide el Informe.

Un resumen mas largo de cada funcion, y para que le sirve al Informe,
esta en docs/MODULO_B.md.
"""

import math


def analyze_text(file_path):
    """
    Lee el archivo de texto y calcula, para cada caracter que aparece,
    cuantas veces aparece (cantidad) y que porcentaje del texto ocupa
    (probabilidad).

    Ejemplo: si el texto fuera "aab", el resultado tendria que ser:
        counts = {'a': 2, 'b': 1}
        probabilities = {'a': 0.66..., 'b': 0.33...}

    Recibe:
        file_path -- la ruta del archivo de texto, por ejemplo
                      "data/example_text.txt"
    Devuelve:
        una tupla (counts, probabilities):
        - counts es un diccionario {caracter: cantidad de veces que aparece}
        - probabilities es un diccionario {caracter: probabilidad}
    """
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Contamos cuantas veces aparece cada caracter en el texto
    counts = {}
    for char in text:
        if char in counts:
            counts[char] = counts[char] + 1
        else:
            counts[char] = 1

    # A partir de las cantidades, calculamos la probabilidad de cada caracter
    total_chars = len(text)
    probabilities = {}
    for char, count in counts.items():
        probabilities[char] = count / total_chars

    return counts, probabilities


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
    # La formula de la entropia es: H = - suma( p * log2(p) ) para cada
    # caracter. El "-" esta porque log2(p) da negativo (p es un numero
    # entre 0 y 1), y asi el resultado final queda positivo.
    entropy = 0
    for prob in probabilities.values():
        entropy = entropy - prob * math.log2(prob)
    return entropy


def generate_huffman_code(probabilities):
    """
    Arma el "diccionario de codigos" de Huffman: a cada caracter le
    asigna una palabra hecha de 0s y 1s. Los caracteres mas frecuentes
    tendrian que quedar con codigos mas cortos.

    Como funciona (resumen): se arma un arbol de abajo hacia arriba.
    Se empieza con un "nodo" por cada caracter (con su probabilidad).
    En cada paso, se toman los DOS nodos con menor probabilidad y se
    juntan en un nodo nuevo (cuya probabilidad es la suma de esos dos).
    Se repite hasta que queda un solo nodo: la raiz del arbol. El
    codigo de cada caracter es el camino desde la raiz hasta el,
    poniendo un '0' cada vez que se va para la izquierda y un '1' cada
    vez que se va para la derecha.

    Recibe:
        probabilities -- el diccionario {caracter: probabilidad}
    Devuelve:
        un diccionario {caracter: codigo}, donde el codigo es un texto
        de '0's y '1's, por ejemplo {'a': '0', 'b': '10', 'c': '11'}
    """
    # Empezamos con un nodo "hoja" por cada caracter
    nodes = []
    for char, prob in probabilities.items():
        nodes.append({"prob": prob, "char": char})

    # Caso especial: si el texto tiene un solo caracter distinto, no hay
    # nada para combinar. Le asignamos el codigo '0' directamente.
    if len(nodes) == 1:
        return {nodes[0]["char"]: "0"}

    # Vamos combinando de a dos nodos (los de menor probabilidad) hasta
    # que quede uno solo: la raiz del arbol
    while len(nodes) > 1:
        # Ordenamos por probabilidad, de menor a mayor
        nodes.sort(key=lambda node: node["prob"])

        # Sacamos los dos con menor probabilidad
        left = nodes.pop(0)
        right = nodes.pop(0)

        # Los combinamos en un nodo nuevo, y lo volvemos a meter en la lista
        merged = {"prob": left["prob"] + right["prob"], "left": left, "right": right}
        nodes.append(merged)

    root = nodes[0]

    # Recorremos el arbol desde la raiz para armar el codigo de cada caracter
    code = {}
    _walk_huffman_tree(root, "", code)
    return code


def _walk_huffman_tree(node, path_so_far, code):
    """
    Funcion auxiliar de generate_huffman_code: recorre el arbol de
    Huffman (de la raiz hacia las hojas) y va completando el
    diccionario {caracter: codigo}.

    Recibe:
        node -- el nodo actual del arbol
        path_so_far -- el codigo acumulado para llegar hasta este nodo
        code -- el diccionario que se va completando a medida que
                 encontramos caracteres (se modifica directamente,
                 no hace falta que esta funcion devuelva nada)
    """
    if "char" in node:
        # Es una hoja: encontramos un caracter, guardamos su codigo
        code[node["char"]] = path_so_far
    else:
        # Es un nodo interno: seguimos por los dos caminos posibles
        _walk_huffman_tree(node["left"], path_so_far + "0", code)
        _walk_huffman_tree(node["right"], path_so_far + "1", code)


def is_prefix_code(code):
    """
    Verifica que el codigo sea un codigo prefijo: que ninguna palabra de
    codigo sea, al mismo tiempo, el comienzo de otra palabra de codigo.
    Esto es justamente lo que permite decodificar sin ambiguedad (ver
    decode_bits) -- por eso vale la pena chequearlo.

    Ejemplo: {'a': '0', 'b': '10', 'c': '11'} SI es prefijo (ninguno
    empieza igual que otro). En cambio {'a': '0', 'b': '01'} NO lo es,
    porque el codigo de 'a' ('0') es el comienzo del codigo de 'b' ('01').

    Recibe:
        code -- el diccionario {caracter: codigo}
    Devuelve:
        True si es codigo prefijo, False si no
    """
    codes = list(code.values())
    for i, code_a in enumerate(codes):
        for code_b in codes[i + 1:]:
            if code_a.startswith(code_b) or code_b.startswith(code_a):
                return False
    return True


def calculate_lengths(code, probabilities):
    """
    Calcula que tan bueno es el codigo que armamos: la longitud minima
    posible (segun la entropia), el promedio real de longitud de las
    palabras de codigo, la varianza, y la eficiencia.

    Recibe:
        code -- el diccionario {caracter: codigo} de generate_huffman_code
        probabilities -- el diccionario {caracter: probabilidad}
    Devuelve:
        un diccionario con las claves 'min_length', 'avg_length',
        'variance' y 'efficiency'
    """
    # La longitud minima teorica es la entropia: Lmin = H(texto)
    min_length = calculate_entropy(probabilities)

    # El promedio real: para cada caracter, su probabilidad multiplicada
    # por la longitud de su codigo, todo sumado
    avg_length = 0
    for char, prob in probabilities.items():
        code_length = len(code[char])
        avg_length = avg_length + prob * code_length

    # La varianza: que tan lejos esta, en promedio, la longitud de cada
    # codigo respecto del promedio (elevado al cuadrado, para que no se
    # cancelen los que estan por arriba con los que estan por abajo)
    variance = 0
    for char, prob in probabilities.items():
        code_length = len(code[char])
        variance = variance + prob * (code_length - avg_length) ** 2

    # La eficiencia dice que tan cerca esta nuestro codigo del ideal
    # teorico: 1.0 (100%) seria un codigo perfecto, que ocupa exactamente
    # lo que dice la entropia. Cuanto mas cerca de 1.0, mejor.
    efficiency = min_length / avg_length

    return {
        "min_length": min_length,
        "avg_length": avg_length,
        "variance": variance,
        "efficiency": efficiency,
    }


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
    bits = ""
    for char in text:
        bits = bits + code[char]
    return bits


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
    # Damos vuelta el diccionario: en vez de {caracter: codigo},
    # queremos {codigo: caracter}, para poder buscar al reves
    code_to_char = {}
    for char, char_code in code.items():
        code_to_char[char_code] = char

    # Vamos juntando bits en "buffer" hasta que forman un codigo
    # conocido. Como el codigo de Huffman es prefijo (ningun codigo es
    # el comienzo de otro), en cuanto el buffer coincide con un codigo
    # sabemos con seguridad que es ese caracter, sin ambiguedad.
    text = ""
    buffer = ""
    for bit in bits:
        buffer = buffer + bit
        if buffer in code_to_char:
            text = text + code_to_char[buffer]
            buffer = ""

    return text


def save_text(text, output_path):
    """
    Guarda un texto en un archivo .txt.

    Recibe:
        text -- el texto a guardar
        output_path -- donde guardarlo, por ejemplo
                        "results/run1_received.txt"
    No devuelve nada, solo crea el archivo.
    """
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)
