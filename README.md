# TP TA137 – Sistema de Comunicaciones Digitales

Este es el código del TP integrador de Comunicaciones Digitales. Por ahora tiene la primera parte completa: leer un texto, codificarlo/decodificarlo con el algoritmo de Huffman, y armar el informe con las tablas que pide el enunciado. Las partes que faltan (canal, modulación, etc.) se van a ir agregando más adelante, a medida que las veamos en clase — no hace falta que esté todo armado desde el principio.

## Qué hay en cada archivo

- `src/main.py` — el programa principal. Es el que se ejecuta, y llama en orden a las funciones de los demás archivos.
- `src/cli.py` — se encarga de leer los parámetros por consola y mostrar los mensajes. No hace falta tocarlo para hacer el TP.
- `src/source.py` — las funciones de Huffman (Módulo B). **Ya está completo.**
- `src/report.py` — arma el informe (tablas y ejemplos) en un archivo `.md` dentro de `results/`, a partir de lo que calcula `source.py`.
- `checks/verify_huffman.py` — un script aparte (no lo usa el programa) que compara nuestro Huffman contra una librería de Python, solo para verificar que da resultados igual de buenos.
- `data/` — el archivo de texto que se usa como ejemplo.
- `results/` — acá se guardan el texto recibido y el informe cada vez que se corre el programa.
- `docs/ARCHITECTURE.md` — explica el diagrama de bloques del TP y qué parte está hecha y cuál falta.
- `docs/MODULO_B.md` — el checklist detallado de todo lo que pedía Módulo B (ya completo).

## Instalación (una sola vez)

1. Instalar [Python](https://www.python.org/downloads/) (versión 3.9 o más nueva) si no lo tenés.
2. Abrir una terminal en la carpeta del proyecto y crear un entorno virtual (esto es como una "caja" propia del proyecto para instalar cosas sin afectar el resto de la computadora):

   ```bash
   python -m venv .venv
   ```

3. Activar ese entorno:

   ```bash
   source .venv/bin/activate
   ```

   En Windows es `.venv\Scripts\activate`.

4. Instalar las librerías que va a necesitar el proyecto (por ahora, para la parte de Huffman, ni siquiera hace falta este paso — pero no está de más dejarlo listo):

   ```bash
   pip install -r requirements.txt
   ```

Nota: en algunas instalaciones de Python hay que escribir `python3` en vez de `python` en los comandos de arriba.

## Cómo correrlo

Importante: los comandos se corren siempre desde la carpeta principal del proyecto (`tp-taller-com-dig/`), no desde adentro de `src/`.

Para probar que todo esté bien instalado (esto no ejecuta Huffman todavía, solo revisa que el archivo de texto se pueda leer):

```bash
python src/main.py --dry-run
```

Para correr el programa de verdad:

```bash
python src/main.py
```

Esto codifica el texto de ejemplo con Huffman, lo decodifica, y guarda dos archivos en `results/`: el texto recibido (`run1_received.txt`) y el informe con las tablas (`run1_informe_modulo_b.md`).

## Cómo seguimos

Módulo B (Huffman) ya está completo — ver el detalle en [docs/MODULO_B.md](docs/MODULO_B.md). El próximo paso es Módulo C (codificación de canal), que se va a agregar en un archivo nuevo (`src/channel.py` o similar) siguiendo el mismo esquema: funciones explicadas paso a paso, y `main.py` las va a ir llamando en el lugar que ya está marcado en el código.
