# TP TA137 – Sistema de Comunicaciones Digitales

Este es el código del TP integrador de Comunicaciones Digitales. Por ahora solo tiene la primera parte: leer un texto y codificarlo/decodificarlo con el algoritmo de Huffman. Las partes que faltan (canal, modulación, etc.) se van a ir agregando más adelante, a medida que las veamos en clase — no hace falta que esté todo armado desde el principio.

## Qué hay en cada archivo

- `src/main.py` — el programa principal. Es el que se ejecuta, y llama en orden a las funciones de los demás archivos.
- `src/cli.py` — se encarga de leer los parámetros por consola y mostrar los mensajes. No hace falta tocarlo para hacer el TP.
- `src/source.py` — **acá es donde hay que trabajar ahora.** Tiene las funciones de Huffman, todas explicadas pero sin hacer todavía.
- `data/` — el archivo de texto que se usa como ejemplo.
- `results/` — acá se va a guardar el resultado cuando corramos el programa.
- `docs/ARCHITECTURE.md` — explica el diagrama de bloques del TP y qué parte está hecha y cuál falta.

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

Como las funciones de Huffman todavía no están hechas, esto va a terminar con un error que dice `NotImplementedError` — es lo esperado por ahora. A medida que se vayan completando las funciones en `src/source.py`, el programa va a ir avanzando más.

## Cómo seguimos

Todo el trabajo por ahora está en `src/source.py`. El archivo tiene 7 funciones, cada una con una explicación de qué tiene que hacer, qué recibe y qué tiene que devolver (con un ejemplo). Se puede ir haciendo una por una, sin necesidad de terminarlas todas juntas — no hace falta entender el archivo entero para empezar por la primera.
