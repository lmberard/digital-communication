# Módulo B — Checklist (Huffman)

Esta es la lista de todo lo que pide el enunciado para el Módulo B: las funciones de código y, al lado, para qué parte del Informe sirve cada una. La idea es ir tildando a medida que se completa cada cosa.

## 1. Funciones de código (`src/source.py`)

| # | Función | Qué hace (enunciado) | Para qué parte del Informe sirve |
|---|---|---|---|
| ☑ | `analyze_text` | Lee el .txt y calcula la cantidad y la probabilidad de cada carácter (punto B.1) | Informe **(a)** |
| ☑ | `calculate_entropy` | Calcula la entropía de la fuente (punto B.2) | Informe **(e)** |
| ☑ | `generate_huffman_code` | Arma el diccionario de códigos de Huffman (punto B.3) | Informe **(a)**, y es la base para **(b)** y **(c)** |
| ☑ | `calculate_lengths` | Longitud mínima, promedio y varianza del código (puntos B.4 y B.5) | Informe **(e)** |
| ☑ | `encode_text` | Codifica el texto completo a bits, usando el código de arriba (punto B.6) | Informe **(d)** y **(f)** |
| ☑ | `decode_bits` | Decodifica los bits de vuelta a texto — lado Receptor (punto B.7) | Informe **(d)** |
| ☑ | `save_text` | Guarda el texto decodificado en un archivo — lado Receptor (punto B.8) | No se pide directo en el Informe, es para que el programa ande de punta a punta |

## 2. ✅ Cosas que pedía el Informe y que no estaban cubiertas por las 7 funciones (ya resueltas)

- ☑ **Cantidad de apariciones de cada carácter.** `analyze_text` devuelve `(counts, probabilities)`, dos diccionarios en vez de uno solo.
- ☑ **Eficiencia del código.** `calculate_lengths` ahora también devuelve la clave `'efficiency'` (= `min_length / avg_length`). Probado: en el caso clásico (donde Huffman es óptimo) da exactamente `1.0`; con el texto real da `0.9926` (99.27%).
- ☑ **Verificación de código prefijo.** Nueva función `is_prefix_code(code)` en `src/source.py`. Probada con un caso válido, uno inválido a propósito, y con el código real del texto de ejemplo (da `True`).

## 3. Qué hay que mostrar en el Informe (letras a-f del enunciado)

| Ítem | Qué pide el enunciado | De dónde sale |
|---|---|---|
| **(a)** | Tabla con la cantidad, la probabilidad y el código de Huffman de cada carácter | `analyze_text` (con la cantidad agregada) + `generate_huffman_code` |
| **(b)** | Verificar que el código es "prefijo" (que ninguna palabra de código es el comienzo de otra) | `is_prefix_code` |
| **(c)** | Descripción breve de las características del código obtenido | Texto para el Informe, mirando los resultados de `generate_huffman_code` |
| **(d)** | Una línea de texto de ejemplo: original → en bits → decodificada de nuevo | `encode_text` + `decode_bits` |
| **(e)** | Tabla con: entropía, longitud mínima, longitud promedio, varianza, eficiencia, y la longitud de un código de largo fijo (ASCII extendido = siempre 8 bits por carácter) | `calculate_entropy` + `calculate_lengths` (ya trae `efficiency` incluida) + el dato fijo "8 bits" |
| **(f)** | Tabla: cuántos bits hacen falta en total para todo el texto con Huffman vs. con código de largo fijo | Cantidad total = largo del resultado de `encode_text`, comparado contra "cantidad de caracteres del texto × 8" |

## Cómo seguir

1. ~~Empezar por `analyze_text`~~ — listo.
2. ~~`generate_huffman_code`~~ — listo (probado con el ejemplo clásico de 3 símbolos, con "aab", y con el texto de ejemplo: da código prefijo válido).
3. ~~`encode_text`~~ — listo (probado con el ejemplo del docstring y con el texto real: 323 caracteres se convirtieron en 1478 bits, menos que los 2584 que ocuparía con ASCII de 8 bits fijos).
4. ~~`decode_bits`~~ — listo (probado que el texto recuperado es idéntico al original, carácter por carácter).
5. ~~`save_text`~~ — listo. **El programa ya corre de punta a punta sin errores** (`python src/main.py`): guarda el texto recibido en `results/run1_received.txt`, y coincide 100% con el original.
6. ~~`calculate_entropy`~~ — listo (probado con casos conocidos: 3 símbolos da 1.5, 4 equiprobables da exactamente log2(4)=2.0, un solo carácter da 0.0; con el texto real da 4.54 bits, un poco menos que el promedio real de 4.575 bits/carácter que ya habíamos medido — tiene sentido, Huffman es casi óptimo).
7. ~~`calculate_lengths`~~ — listo. **Las 7 funciones de Módulo B están hechas.** Probado con el caso clásico (`avg_length` da exactamente igual a `min_length`, porque ahí Huffman es óptimo) y con el texto real (`min_length` ≤ `avg_length`, como tiene que ser, y `avg_length × cantidad de caracteres` da los mismos 1478 bits que ya habíamos medido con `encode_text`).
8. ~~Eficiencia y verificación de código prefijo~~ — listo (sección 2). Ya no queda ninguna función pendiente.
9. Lo único que falta ahora es armar el Informe en sí: las tablas y ejemplos de la sección 3, usando lo que ya devuelven las funciones. La letra **(c)** es la única que es puro texto (no sale de ninguna función) — hay que escribirla a partir de lo que se observa en los resultados.
