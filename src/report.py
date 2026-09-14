"""
Arma el Informe en un archivo markdown (.md), con las tablas y ejemplos
que pide el enunciado (ver docs/MODULO_B.md, seccion 3 "Que hay que
mostrar en el Informe").

Este archivo se encarga solo de darle formato "para humanos" a los
resultados que ya calculamos en source.py (y, mas adelante, en los
demas modulos) -- no repite la logica de Huffman, solo la usa. La idea
es que cuando main.py sume mas pasos (codificacion de canal, modulacion,
etc.), cada modulo tenga su propia funcion de informe aca, en vez de
mezclar "calcular" con "armar tablas" en cada archivo.
"""

import source


def generate_module_b_report(text, counts, probabilities, code, bits, received_text, output_path):
    """
    Arma el informe del Modulo B (Huffman): las 6 partes que pide el
    enunciado, letras (a) a (f), y lo guarda como un archivo .md.

    Recibe:
        text -- el texto original completo
        counts -- {caracter: cantidad}, de analyze_text
        probabilities -- {caracter: probabilidad}, de analyze_text
        code -- {caracter: codigo}, de generate_huffman_code
        bits -- el texto ya codificado en 0s y 1s, de encode_text
        received_text -- el texto decodificado, de decode_bits
        output_path -- donde guardar el informe, por ejemplo
                        "results/run1_informe_modulo_b.md"
    No devuelve nada, solo crea el archivo.
    """
    lengths = source.calculate_lengths(code, probabilities)
    prefix_ok = source.is_prefix_code(code)

    # De mas frecuente a menos frecuente, para que la tabla se lea mejor
    caracteres_ordenados = sorted(counts.items(), key=lambda item: -item[1])

    lines = []
    lines.append("# Informe Modulo B — Codificación de fuente (Huffman)")
    lines.append("")

    # --- (a) Tabla de caracteres, cantidad, probabilidad y codigo ---
    lines.append("## (a) Probabilidades y código de cada carácter")
    lines.append("")
    lines.append("| Carácter | Cantidad | Probabilidad | Código Huffman |")
    lines.append("|---|---|---|---|")
    for char, count in caracteres_ordenados:
        lines.append(
            f"| {_mostrar_caracter(char)} | {count} | {probabilities[char]:.4f} | {code[char]} |"
        )
    lines.append("")

    # --- (b) Verificacion de codigo prefijo ---
    lines.append("## (b) Verificación de código prefijo")
    lines.append("")
    if prefix_ok:
        lines.append(
            "El código generado **sí** es un código prefijo: ninguna palabra de código "
            "es el comienzo de otra, por eso se puede decodificar sin ambigüedad."
        )
    else:
        lines.append("El código generado **no** es un código prefijo (esto no debería pasar con Huffman).")
    lines.append("")

    # --- (c) Descripcion breve de las caracteristicas del codigo ---
    char_mas_frecuente, cantidad_mas_frecuente = caracteres_ordenados[0]
    longitud_maxima = max(len(c) for c in code.values())
    longitud_minima_real = min(len(c) for c in code.values())
    lines.append("## (c) Características del código obtenido")
    lines.append("")
    lines.append(
        f"El texto tiene {len(counts)} caracteres distintos. "
        f"El más frecuente es {_mostrar_caracter(char_mas_frecuente)} "
        f"(aparece {cantidad_mas_frecuente} veces) y recibió el código más corto. "
        f"Las palabras de código van de {longitud_minima_real} a {longitud_maxima} bits: "
        f"los caracteres frecuentes quedaron con códigos cortos, y los que casi no "
        f"aparecen, con códigos largos — que es justamente la idea de Huffman."
    )
    lines.append("")

    # --- (d) Ejemplo de una linea codificada y decodificada ---
    primera_linea = text.split("\n")[0]
    primera_linea_bits = source.encode_text(primera_linea, code)
    primera_linea_decodificada = source.decode_bits(primera_linea_bits, code)
    lines.append("## (d) Ejemplo: una línea codificada y decodificada")
    lines.append("")
    lines.append(f"- Texto original: `{primera_linea}`")
    lines.append(f"- Codificado: `{primera_linea_bits}`")
    lines.append(f"- Decodificado: `{primera_linea_decodificada}`")
    lines.append("")

    # --- (e) Tabla de entropia, longitudes y eficiencia ---
    lines.append("## (e) Entropía, longitudes y eficiencia")
    lines.append("")
    lines.append("| Métrica | Valor |")
    lines.append("|---|---|")
    lines.append(f"| Entropía (bits/carácter) | {lengths['min_length']:.4f} |")
    lines.append(f"| Longitud mínima (Lmin) | {lengths['min_length']:.4f} |")
    lines.append(f"| Longitud promedio | {lengths['avg_length']:.4f} |")
    lines.append(f"| Varianza | {lengths['variance']:.4f} |")
    lines.append(f"| Eficiencia | {lengths['efficiency']:.4f} ({lengths['efficiency'] * 100:.2f}%) |")
    lines.append("| Código de longitud fija (ASCII extendido) | 8 bits/carácter |")
    lines.append("")

    # --- (f) Tabla de bits totales: Huffman vs. longitud fija ---
    bits_huffman = len(bits)
    bits_fijo = len(text) * 8
    ahorro_porcentaje = (1 - bits_huffman / bits_fijo) * 100
    lines.append("## (f) Bits totales: Huffman vs. código de longitud fija")
    lines.append("")
    lines.append("| Método | Bits totales |")
    lines.append("|---|---|")
    lines.append(f"| Huffman (nuestro código) | {bits_huffman} |")
    lines.append(f"| Longitud fija (8 bits/carácter) | {bits_fijo} |")
    lines.append("")
    lines.append(
        f"Huffman ocupa {bits_fijo - bits_huffman} bits menos "
        f"({ahorro_porcentaje:.1f}% de ahorro) respecto al código de longitud fija."
    )
    lines.append("")

    # --- Chequeo extra: que el texto recibido sea igual al original ---
    lines.append("## Verificación final")
    lines.append("")
    lines.append(f"¿El texto decodificado es igual al original?: **{received_text == text}**")
    lines.append("")

    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))


def _mostrar_caracter(char):
    """
    Funcion auxiliar: algunos caracteres (espacio, salto de linea, etc.)
    no se ven bien tal cual adentro de una tabla, asi que les damos un
    nombre mas claro para mostrar.
    """
    nombres = {
        " ": "(espacio)",
        "\n": "(salto de línea)",
        "\t": "(tab)",
    }
    return nombres.get(char, char)
