from abc import ABC, abstractmethod

import numpy as np
import matplotlib.pyplot as plt

from collections.abc import Callable

from pathlib import Path
from typing import List, Any
from utils import BLUE, RESET

# Interfaz base que todos los reporters deben implementar.
# Permite que los módulos del pipeline reporten resultados sin conocer
# el destino concreto (terminal, archivo, silencioso, etc.).
class Reporter(ABC):
    @abstractmethod
    def report_results(self, file_name: str, headers: List[str], data: List[List[Any]]) -> None:
        # Guarda una tabla de datos tabulares (ej: tabla Huffman) en algún destino.
        pass

    @abstractmethod
    def append_metrics(self, from_encoder: str, lines: str) -> None:
        # Acumula líneas de métricas de un módulo para incluirlas en el reporte final.
        pass

    @abstractmethod
    def append_line(self, from_encoder: str, color: str, line: str) -> None:
        # Emite una línea de log con el nombre del módulo que la genera.
        pass

    @abstractmethod
    def graph(self, graph_name: str, axis: np.ndarray, graph: Callable[[np.ndarray], None]) -> None:
        # Renderiza un gráfico dado un nombre y una función que dibuja sobre el eje.
        pass

    @abstractmethod
    def show(self) -> None:
        # Finaliza el reporte (ej: escribe el archivo de métricas al disco).
        pass

# Reporter silencioso para usar en tests.
# Implementa la interfaz sin hacer nada, evitando efectos de I/O durante las pruebas.
class EmptyReporter(Reporter):
    def report_results(self, file_name: str, headers: List[str], data: List[List[Any]]):
        pass

    def append_metrics(self, from_encoder: str, lines: str) -> None:
        pass

    def append_line(self, from_encoder: str, color: str, line: str):
        pass

    def graph(self, graph_name: str, axis: np.ndarray, graph: Callable[[np.ndarray], None]) -> None:
        plt.close()
        pass

    def show(self):
        pass

# Reporter completo: imprime a consola y persiste resultados en disco.
# Se usa en ejecución normal del pipeline.
class ReporterTerminal(Reporter):
    def __init__(self, out_prefix: str, encoding: str = "utf-8"):
        self.out_prefix = out_prefix
        self.encoding = encoding
        # Diccionario que acumula las métricas por módulo para el archivo metricas.md
        self.metric_encoders = {}

    def report_results(self, file_name: str, headers: List[str], data: List[List[Any]]):
        # Escribe la tabla como CSV en {out_prefix}/{file_name}
        csv_path = Path(f"{self.out_prefix}/{file_name}")
        with csv_path.open("w", encoding=self.encoding) as f:
            f.write(",".join(headers) + "\n")
            for line in data:
                f.write(",".join(line) + "\n")

        self.append_line("Reporter", BLUE, f"CSV → {csv_path}")
        return csv_path

    def append_metrics(self, from_encoder: str, lines: str) -> None:
        # Agrupa las métricas por módulo; se vuelcan todas juntas en show()
        if not from_encoder in self.metric_encoders:
            self.metric_encoders[from_encoder] = []
        self.metric_encoders[from_encoder].append(lines)

    def append_line(self, from_encoder: str, color: str, line: str):
        # Imprime en consola con color y el nombre del módulo entre corchetes
        print(f"{color}[{from_encoder}]{RESET} {line}")

    def graph(self, graph_name: str, axis: np.ndarray, graph: Callable[[np.ndarray], None]) -> None:
        # Ejecuta la función de dibujo sobre el eje y guarda la figura como PNG
        graph_path = f"{self.out_prefix}/{graph_name}"
        graph(axis)
        plt.tight_layout()
        plt.savefig(graph_path)
        plt.close()
        self.append_line("Reporter", BLUE, f"Gráfico → {graph_path}")
        return graph_path

    def show(self):
        # Escribe todas las métricas acumuladas en {out_prefix}/metricas.md
        metrics = Path(f"{self.out_prefix}/metricas.md")
        metric_lines = []
        for from_encoder, lines in self.metric_encoders.items():
            metric_lines.append(f"### Resultados {from_encoder}")
            metric_lines += lines
            metric_lines.append("\n")

        metrics.write_text("\n".join(metric_lines), encoding = self.encoding)

# Reporter para el modo de análisis (Módulo F).
# Solo imprime a consola; no guarda tablas ni gráficos porque el análisis
# genera sus propios archivos directamente.
class ReporterAnalysis(Reporter):
    def report_results(self, file_name: str, headers: List[str], data: List[List[Any]]):
        return None

    def append_metrics(self, from_encoder: str, lines: str) -> None:
        return None

    def append_line(self, from_encoder: str, color: str, line: str):
        print(f"{color}[{from_encoder}]{RESET} {line}")

    def graph(self, graph_name: str, axis: np.ndarray, graph: Callable[[np.ndarray], None]) -> None:
        plt.close()
        return None

    def show(self):
        return None

def _printable(ch: str) -> str:
    # Convierte caracteres de control e invisibles a una representación legible
    # para mostrarlos en la tabla Huffman (ej: "\n" → "\\n", espacio → "␠")
    if ch == "\n": return "\\n"
    if ch == "\t": return "\\t"
    if ch == "\r": return "\\r"
    if ch == " ":  return "␠"
    return ch

def _first_nonempty_line(text: str) -> str:
    # Devuelve la primera línea no vacía del texto.
    # Se usa para mostrar una muestra del contenido en los logs del pipeline.
    for ln in text.splitlines():
        if ln.strip() != "":
            return ln
    return text.splitlines()[0] if "\n" in text else text
