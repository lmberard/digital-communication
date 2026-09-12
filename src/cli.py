"""
Todo lo que es leer los parametros de la linea de comandos, leer el
archivo de entrada, y los mensajes que se muestran por pantalla vive
aca, para que main.py se dedique solo a organizar los pasos del
programa (y sea mas facil de leer).
"""

import argparse
from pathlib import Path


def parse_args():
    """Define y lee los parametros que se le pueden pasar al programa
    por linea de comandos."""
    parser = argparse.ArgumentParser(
        description="TP de Comunicaciones Digitales: por ahora, codifica y decodifica un texto con Huffman."
    )
    parser.add_argument(
        "--input",
        default="data/example_text.txt",
        help="Archivo de texto a usar (por defecto: data/example_text.txt).",
    )
    parser.add_argument(
        "--output-prefix",
        default="results/run1",
        help="Con que nombre guardar los resultados (por defecto: results/run1).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Solo revisa que el archivo de entrada se pueda leer, sin correr Huffman.",
    )
    return parser.parse_args()


def load_input_text(args):
    """Lee el archivo de entrada y crea la carpeta de resultados si
    todavia no existe. Devuelve el texto leido."""
    text = Path(args.input).read_text(encoding="utf-8")
    Path(args.output_prefix).parent.mkdir(parents=True, exist_ok=True)
    return text


def build_output_path(args):
    """Arma el nombre del archivo donde se va a guardar el texto que
    llega al final del programa."""
    return f"{args.output_prefix}_received.txt"


def print_parameters(args, text):
    """Muestra por pantalla con que archivo se va a trabajar."""
    print("Parametros:")
    print(f"  Archivo de entrada: {args.input} ({len(text)} caracteres)")
    print(f"  Resultados en:      {args.output_prefix}")


def setup():
    """Lee los parametros, carga el archivo de entrada y muestra el
    resumen por pantalla. Devuelve (args, text)."""
    args = parse_args()
    text = load_input_text(args)
    print_parameters(args, text)
    return args, text


def print_dry_run_notice():
    """Mensaje que se muestra cuando se corre con --dry-run."""
    print("\n[dry-run] Se pudo leer el archivo de entrada bien. No se ejecuto nada mas.")


def print_results(output_path, received_text, original_text):
    """Muestra el resultado final: donde quedo guardado el texto
    recibido, y si es igual al texto original."""
    print(f"\nTexto recibido guardado en: {output_path}")
    print(f"¿Es igual al original?: {received_text == original_text}")
