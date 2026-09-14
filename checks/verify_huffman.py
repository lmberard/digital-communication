"""
Este script no es parte del programa (main.py no lo usa para nada). Es
solo para comparar nuestra generate_huffman_code, la que escribimos a
mano en src/source.py, contra la del paquete "huffman" de PyPI, y
confirmar que da resultados igual de buenos.

Necesita el paquete "huffman" instalado (no esta en requirements.txt a
proposito, porque no se usa en el programa real, solo aca):

    pip install huffman

Como correrlo (desde la raiz del proyecto):

    python checks/verify_huffman.py
"""

import sys
from pathlib import Path

# Para que este script encuentre src/source.py sin importar desde donde
# se lo corra
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import source

try:
    import huffman as huffman_lib
except ImportError:
    print("Falta el paquete 'huffman'. Instalalo con: pip install huffman")
    sys.exit(1)


def comparar(probabilities, nombre):
    """
    Arma el codigo con las dos implementaciones y compara que tan
    buenas son. Ojo: no comparamos que el codigo de cada caracter sea
    IGUAL en las dos (eso puede variar), sino que las dos ocupen la
    misma cantidad de bits en promedio.
    """
    our_code = source.generate_huffman_code(probabilities)
    lib_code = dict(huffman_lib.codebook(list(probabilities.items())))

    print(f"--- {nombre} ---")
    print("Nuestro codigo:  ", our_code)
    print("Codigo de la lib:", lib_code)

    our_avg = source.calculate_lengths(our_code, probabilities)["avg_length"]
    lib_avg = source.calculate_lengths(lib_code, probabilities)["avg_length"]

    print(f"Promedio de bits/caracter (nuestro):  {our_avg:.4f}")
    print(f"Promedio de bits/caracter (libreria): {lib_avg:.4f}")

    # Redondeamos antes de comparar para no fallar por diferencias de
    # punto flotante microscopicas (cosas como 0.1 + 0.2 no dan
    # exactamente 0.3 en ninguna computadora, por como se representan
    # los numeros con decimales)
    if round(our_avg, 6) == round(lib_avg, 6):
        print("Dan igual de bien -> OK")
    else:
        print("Dan distinto -> revisar!")
    print()


# Ejemplo facil de seguir a mano: 'a' aparece la mitad de las veces, y
# 'b' y 'c' un cuarto cada uno. Haciendolo en papel, el resultado
# esperado es que 'a' quede con el codigo mas corto (1 bit) y 'b'/'c'
# un poco mas largos (2 bits cada uno) -> promedio de 1.5 bits/caracter.
comparar({"a": 0.5, "b": 0.25, "c": 0.25}, "Ejemplo simple (a, b, c)")

# Y tambien lo probamos con el texto real del proyecto, un caso mas
# grande (49 caracteres distintos), para no quedarnos solo con el
# ejemplo chiquito
_, probabilities = source.analyze_text("data/example_text.txt")
comparar(probabilities, "Texto real (data/example_text.txt)")


# ----------------------------------------------------------------------
# ¿Por que no usamos directamente la libreria en src/source.py?
#
# Porque ya la comparamos ahi arriba y da exactamente los mismos
# resultados (el mismo promedio de bits por caracter) que la nuestra.
# El codigo exacto de cada caracter puede variar un poco entre las dos
# (Huffman no tiene una unica solucion posible: cuando hay
# probabilidades empatadas, se pueden combinar en distinto orden), pero
# la cantidad de bits que ocupa el texto final termina siendo la misma.
#
# Como la nuestra ya esta hecha, probada, y funciona igual de bien, la
# dejamos como esta en vez de reemplazarla:
#   - Es mas facil de explicar en el informe: todo el algoritmo esta
#     ahi, comentado paso a paso, en vez de ser una funcion importada
#     de una libreria externa que nadie del grupo escribio.
#   - No suma una dependencia mas al proyecto para resolver algo que ya
#     resolvimos nosotros mismos.
# ----------------------------------------------------------------------
