# Módulo B — Checklist (Huffman)

Esta es la lista de todo lo que pide el enunciado para el Módulo B: las funciones de código y, al lado, para qué parte del Informe sirve cada una. La idea es ir tildando a medida que se completa cada cosa.

## 1. Funciones de código (`src/source.py`)

| # | Función | Qué hace (enunciado) | Para qué parte del Informe sirve |
|---|---|---|---|
| ☑ | `analyze_text` | Lee el .txt y calcula la cantidad y la probabilidad de cada carácter (punto B.1) | Informe **(a)** |
| ☐ | `calculate_entropy` | Calcula la entropía de la fuente (punto B.2) | Informe **(e)** |
| ☑ | `generate_huffman_code` | Arma el diccionario de códigos de Huffman (punto B.3) | Informe **(a)**, y es la base para **(b)** y **(c)** |
| ☐ | `calculate_lengths` | Longitud mínima, promedio y varianza del código (puntos B.4 y B.5) | Informe **(e)** |
| ☑ | `encode_text` | Codifica el texto completo a bits, usando el código de arriba (punto B.6) | Informe **(d)** y **(f)** |
| ☐ | `decode_bits` | Decodifica los bits de vuelta a texto — lado Receptor (punto B.7) | Informe **(d)** |
| ☐ | `save_text` | Guarda el texto decodificado en un archivo — lado Receptor (punto B.8) | No se pide directo en el Informe, es para que el programa ande de punta a punta |

## 2. ⚠️ Cosas que pide el Informe y que no están cubiertas por las 7 funciones

- ☑ **Cantidad de apariciones de cada carácter.** ~~El Informe (a) pide "la cantidad **y** la probabilidad" de cada carácter, pero `analyze_text` hoy solo calcula la probabilidad.~~ Resuelto: `analyze_text` ahora devuelve `(counts, probabilities)`, dos diccionarios en vez de uno solo.
- ☐ **Eficiencia del código.** El Informe (e) pide la eficiencia (entropía dividido longitud promedio), y eso no es ninguno de los puntos B.1 a B.8 — hay que calcularla aparte, usando lo que devuelven `calculate_entropy` y `calculate_lengths`.

## 3. Qué hay que mostrar en el Informe (letras a-f del enunciado)

| Ítem | Qué pide el enunciado | De dónde sale |
|---|---|---|
| **(a)** | Tabla con la cantidad, la probabilidad y el código de Huffman de cada carácter | `analyze_text` (con la cantidad agregada) + `generate_huffman_code` |
| **(b)** | Verificar que el código es "prefijo" (que ninguna palabra de código es el comienzo de otra) | No hay una función pedida para esto puntualmente — hay que armar una chiquita, o revisarlo a mano y explicarlo en el Informe |
| **(c)** | Descripción breve de las características del código obtenido | Texto para el Informe, mirando los resultados de `generate_huffman_code` |
| **(d)** | Una línea de texto de ejemplo: original → en bits → decodificada de nuevo | `encode_text` + `decode_bits` |
| **(e)** | Tabla con: entropía, longitud mínima, longitud promedio, varianza, eficiencia, y la longitud de un código de largo fijo (ASCII extendido = siempre 8 bits por carácter) | `calculate_entropy` + `calculate_lengths` + la eficiencia (punto 2 de arriba) + el dato fijo "8 bits" |
| **(f)** | Tabla: cuántos bits hacen falta en total para todo el texto con Huffman vs. con código de largo fijo | Cantidad total = largo del resultado de `encode_text`, comparado contra "cantidad de caracteres del texto × 8" |

## Cómo seguir

1. ~~Empezar por `analyze_text`~~ — listo.
2. ~~`generate_huffman_code`~~ — listo (probado con el ejemplo clásico de 3 símbolos, con "aab", y con el texto de ejemplo: da código prefijo válido).
3. ~~`encode_text`~~ — listo (probado con el ejemplo del docstring y con el texto real: 323 caracteres se convirtieron en 1478 bits, menos que los 2584 que ocuparía con ASCII de 8 bits fijos).
4. Falta `decode_bits` (el programa ahora se corta ahí) y `save_text`. También sigue pendiente `calculate_entropy`, que no bloquea el resto pero hace falta para el Informe (e).
3. Una vez que las 7 funciones andan, correr `python src/main.py` con el texto de ejemplo y armar las tablas y ejemplos que pide el Informe (sección 3).
