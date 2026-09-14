# Informe Modulo B — Codificación de fuente (Huffman)

## (a) Probabilidades y código de cada carácter

| Carácter | Cantidad | Probabilidad | Código Huffman |
|---|---|---|---|
| (espacio) | 1624 | 0.1687 | 111 |
| e | 873 | 0.0907 | 000 |
| o | 642 | 0.0667 | 1010 |
| t | 612 | 0.0636 | 1001 |
| a | 595 | 0.0618 | 0111 |
| n | 505 | 0.0525 | 0101 |
| i | 495 | 0.0514 | 0100 |
| r | 457 | 0.0475 | 0010 |
| s | 441 | 0.0458 | 11011 |
| l | 365 | 0.0379 | 11001 |
| h | 349 | 0.0362 | 10111 |
| u | 287 | 0.0298 | 10000 |
| d | 274 | 0.0285 | 01101 |
| c | 227 | 0.0236 | 00110 |
| m | 206 | 0.0214 | 110101 |
| g | 183 | 0.0190 | 110001 |
| f | 162 | 0.0168 | 101101 |
| p | 157 | 0.0163 | 100011 |
| y | 157 | 0.0163 | 101100 |
| w | 140 | 0.0145 | 011001 |
| b | 123 | 0.0128 | 001111 |
| , | 108 | 0.0112 | 001110 |
| . | 99 | 0.0103 | 1101001 |
| k | 87 | 0.0090 | 1100001 |
| v | 84 | 0.0087 | 1100000 |
| (salto de línea) | 38 | 0.0039 | 10001010 |
| I | 37 | 0.0038 | 10001000 |
| ' | 35 | 0.0036 | 01100011 |
| q | 22 | 0.0023 | 100010111 |
| B | 18 | 0.0019 | 011000101 |
| S | 17 | 0.0018 | 011000100 |
| M | 14 | 0.0015 | 011000001 |
| x | 13 | 0.0014 | 1101000110 |
| - | 13 | 0.0014 | 1101000111 |
| C | 11 | 0.0011 | 1101000000 |
| T | 11 | 0.0011 | 1101000001 |
| j | 11 | 0.0011 | 1101000010 |
| J | 11 | 0.0011 | 1101000011 |
| H | 10 | 0.0010 | 1000100111 |
| L | 9 | 0.0009 | 1000100100 |
| P | 9 | 0.0009 | 1000100101 |
| W | 9 | 0.0009 | 1000100110 |
| A | 8 | 0.0008 | 0110000100 |
| N | 7 | 0.0007 | 0110000001 |
| F | 6 | 0.0006 | 11010001001 |
| G | 6 | 0.0006 | 11010001010 |
| " | 6 | 0.0006 | 11010001011 |
| D | 5 | 0.0005 | 10001011000 |
| E | 5 | 0.0005 | 10001011001 |
| V | 5 | 0.0005 | 10001011010 |
| ? | 5 | 0.0005 | 10001011011 |
| ; | 5 | 0.0005 | 11010001000 |
| z | 4 | 0.0004 | 01100001010 |
| O | 4 | 0.0004 | 01100001011 |
| Y | 3 | 0.0003 | 01100000000 |
| R | 3 | 0.0003 | 01100000001 |
| U | 2 | 0.0002 | 011000011000 |
| Q | 2 | 0.0002 | 011000011001 |
| K | 2 | 0.0002 | 011000011010 |
| ( | 2 | 0.0002 | 011000011011 |
| ) | 2 | 0.0002 | 011000011100 |
| — | 2 | 0.0002 | 011000011101 |
| ! | 2 | 0.0002 | 011000011110 |
| : | 1 | 0.0001 | 0110000111110 |
| X | 1 | 0.0001 | 0110000111111 |

## (b) Verificación de código prefijo

El código generado **sí** es un código prefijo: ninguna palabra de código es el comienzo de otra, por eso se puede decodificar sin ambigüedad.

## (c) Características del código obtenido

El texto tiene 65 caracteres distintos. El más frecuente es (espacio) (aparece 1624 veces) y recibió el código más corto. Las palabras de código van de 3 a 13 bits: los caracteres frecuentes quedaron con códigos cortos, y los que casi no aparecen, con códigos largos — que es justamente la idea de Huffman.

## (d) Ejemplo: una línea codificada y decodificada

- Texto original: `Classic Lorem Ipsum Filler Text:`
- Codificado: `11010000001100101111101111011010000110111100010010010100010000110101111100010001000111101110000110101111110100010010100110011100100000101111101000001000110100011010010110000111110`
- Decodificado: `Classic Lorem Ipsum Filler Text:`

## (e) Entropía, longitudes y eficiencia

| Métrica | Valor |
|---|---|
| Entropía (bits/carácter) | 4.4613 |
| Longitud mínima (Lmin) | 4.4613 |
| Longitud promedio | 4.4969 |
| Varianza | 2.2035 |
| Eficiencia | 0.9921 (99.21%) |
| Código de longitud fija (ASCII extendido) | 8 bits/carácter |

## (f) Bits totales: Huffman vs. código de longitud fija

| Método | Bits totales |
|---|---|
| Huffman (nuestro código) | 43296 |
| Longitud fija (8 bits/carácter) | 77024 |

Huffman ocupa 33728 bits menos (43.8% de ahorro) respecto al código de longitud fija.

## Verificación final

¿El texto decodificado es igual al original?: **True**
