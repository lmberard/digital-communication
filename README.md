# TP TA137 – Simulación y Análisis de un Sistema de Comunicaciones Digitales

## Estructura del proyecto

```
com-digitales/
├── src/
│   ├── main.py           # Punto de entrada y orquestador CLI
│   ├── cli.py            # Definición de flags y modos de ejecución
│   ├── pipeline.py       # Clase Pipeline y ABC EncoderDecoder
│   ├── file.py           # Módulo A – Lectura/escritura de archivos
│   ├── source.py         # Módulo B – Codificación Huffman
│   ├── modulation.py     # Módulo C – Modulación PSK/FSK
│   ├── channel.py        # Módulo D – Canal AWGN con atenuación opcional
│   ├── cod_channel.py    # Módulo E – Código lineal de bloques [15,5]
│   ├── analysis.py       # Módulo F – Análisis BER/SER vs Eb/N0
│   ├── report.py         # Reporter (Terminal / Analysis / Empty)
│   └── utils.py          # Constantes de color y funciones auxiliares
├── tests/
│   └── test_channel.py
├── data/
│   ├── input/            # Archivos .txt de entrada
│   └── output/           # Resultados generados (texto, métricas, gráficos)
├── generate_report.py    # Genera gráficos PSK vs FSK y REPORTE_ANALISIS_SISTEMA.md
├── requirements.txt
├── INFORME.md            # Informe técnico: teoría, código y análisis por módulo
├── CODE.md               # Referencia técnica de implementación
├── TEORIA.md             # Fundamentos teóricos del sistema
└── CHANGES.md            # Registro de decisiones de diseño
```

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Colocar el archivo de texto de entrada en `data/input/texto.txt`.

## Cómo correr el código

### Pipeline completo (modo por defecto)

Ejecuta todos los módulos: Huffman → Codificación de canal [15,5] → 8-PSK → AWGN → demodulación → decodificación → Huffman inverso.

```bash
python src/main.py
```

Parámetros configurables:

```bash
python src/main.py --in data/input/texto.txt --out-prefix data/output/run1 --ebn0 6.0
```

### Modos alternativos

```bash
# Solo verificar I/O sin procesar
python src/main.py --dry-run

# Solo codificación/decodificación Huffman (Módulo B)
python src/main.py --huffman-only

# Pipeline sin codificación de canal
python src/main.py --without-code

# Análisis completo BER/SER vs Eb/N0 para PSK y FSK (tarda varios minutos)
python src/main.py --analyze-system
```

### Reporte de análisis

Requiere haber ejecutado `--analyze-system` primero. Genera los gráficos PSK vs FSK y el reporte markdown.

```bash
python generate_report.py
```

### Tests

```bash
pytest tests/
```

## Salida generada

Todos los archivos se guardan en `data/output/` con el prefijo indicado (por defecto `run1`):

| Archivo | Contenido |
|---------|-----------|
| `run1/recibido.txt` | Texto final recibido |
| `run1/metricas.md` | H, L̄, η, Pe, Pb, energías por módulo |
| `run1/tabla_huffman.csv` | Tabla de códigos Huffman (char, prob, code, len, ascii) |
| `run1/Contelacion_8-PSK.png` | Constelación teórica |
| `run1/Contelacion_8-PSK_con_datos.png` | Constelación con datos recibidos |

Con `--analyze-system`, se generan además CSVs y gráficos de Pe/Pb vs Eb/N0 en `data/output/`.

## Documentación

- `INFORME.md` — Informe técnico completo: temas aplicados, código referenciado y análisis de resultados por módulo.
- `CODE.md` — Referencia de implementación detallada.
- `TEORIA.md` — Marco teórico del sistema.
