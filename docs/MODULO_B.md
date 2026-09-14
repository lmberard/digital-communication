# Módulo B — Huffman

## Qué es esto y para qué

La idea del Módulo B es agarrar el texto que queremos mandar y convertirlo en una tira de 0s y 1s lo más corta posible, sin perder nada de información (después hay que poder reconstruir el texto exacto, letra por letra).

La forma "obvia" de hacer esto sería usar el mismo largo de código para cada letra (como ASCII, que usa 8 bits para cualquier carácter, ya sea una `a` o una `#`). Huffman es más vivo: mira qué tan seguido aparece cada carácter en el texto, y les da códigos **más cortos a los que aparecen mucho** (como la letra `e` o el espacio) y **más largos a los que casi no aparecen** (como una `x` o un signo raro). En promedio, eso termina ocupando bastante menos espacio que darle a todos el mismo largo — es básicamente la misma idea que un compresor de archivos (zip, etc.).

Todo esto ya está hecho y probado en `src/source.py` (y el informe se arma solo con `src/report.py`, ver más abajo). Si alguien quiere ver los números exactos de qué tan bien funcionó con nuestro texto de ejemplo, están en `results/run1_informe_modulo_b.md` después de correr `python src/main.py`.

## Funciones de código (`src/source.py`)

| ✓ | Función | Qué hace | Punto del enunciado | Informe |
|---|---|---|---|---|
| ✅ | `analyze_text` | Lee el .txt y calcula la cantidad y la probabilidad de aparición de cada carácter | B.1 | (a) |
| ✅ | `calculate_entropy` | Calcula la entropía de la fuente (cuántos bits hacen falta como mínimo, en promedio, por carácter) | B.2 | (e) |
| ✅ | `generate_huffman_code` | Arma el árbol de Huffman y devuelve el diccionario {carácter: código} | B.3 | (a), base de (b) y (c) |
| ✅ | `calculate_lengths` | Longitud mínima (= entropía), longitud promedio, varianza y eficiencia del código | B.4 y B.5 | (e) |
| ✅ | `encode_text` | Codifica el texto completo a bits, usando el código de arriba | B.6 | (d) y (f) |
| ✅ | `decode_bits` | Decodifica los bits de vuelta a texto — lado Receptor | B.7 | (d) |
| ✅ | `save_text` | Guarda el texto decodificado en un archivo — lado Receptor | B.8 | — (para que el programa ande de punta a punta) |
| ✅ | `is_prefix_code` | Verifica que ningún código sea el comienzo de otro (por eso se puede decodificar sin ambigüedad) | — (no es un punto numerado, pero hace falta para el Informe) | (b) |

## Qué hay que mostrar en el Informe

| Ítem | Qué pide el enunciado | De dónde sale |
|---|---|---|
| **(a)** | Tabla con la cantidad, la probabilidad y el código de Huffman de cada carácter | `analyze_text` + `generate_huffman_code` |
| **(b)** | Verificar que el código es "prefijo" (que ninguna palabra de código es el comienzo de otra) | `is_prefix_code` |
| **(c)** | Descripción breve de las características del código obtenido | Se arma sola en `report.py`, a partir del carácter más frecuente y el rango de longitudes de código |
| **(d)** | Una línea de texto de ejemplo: original → en bits → decodificada de nuevo | `encode_text` + `decode_bits` |
| **(e)** | Tabla con: entropía, longitud mínima, longitud promedio, varianza, eficiencia, y la longitud de un código de largo fijo (ASCII extendido = siempre 8 bits por carácter) | `calculate_entropy` + `calculate_lengths` (ya incluye la eficiencia) |
| **(f)** | Tabla: cuántos bits hacen falta en total para todo el texto con Huffman vs. con código de largo fijo | Largo de lo que devuelve `encode_text`, comparado contra "cantidad de caracteres del texto × 8" |

## Qué queda guardado en `results/`

Cada vez que se corre `python src/main.py` (sin `--dry-run`) se generan dos archivos, con el prefijo que se haya usado (`run1` por defecto):

- **`run1_received.txt`** — el texto que quedó después de codificarlo con Huffman y volver a decodificarlo. Tiene que ser idéntico, letra por letra, al archivo de entrada (`data/example_text.txt`) — si no lo es, algo está mal en `encode_text` o `decode_bits`.
- **`run1_informe_modulo_b.md`** — el informe armado por `src/report.py`, con las 6 tablas/ejemplos de la sección de arriba, listo para copiar y pegar (o adaptar) en el informe final que hay que entregar.

Estos dos archivos **no se suben a GitHub** (están en `.gitignore`, adentro de `results/`) porque se generan solos cada vez que alguien corre el programa — no hace falta versionarlos.
