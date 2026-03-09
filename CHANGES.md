# CHANGES.md — Mejoras del proyecto

## Mejoras a nivel código

### Patrón Pipeline (pipeline.py)

La clase `Pipeline` encadena etapas de procesamiento (`EncoderDecoder`) automáticamente: primero ejecuta `encode()` en orden, luego `decode()` en orden inverso. Esto permite agregar o quitar etapas (por ejemplo, codificación de canal) sin modificar el flujo principal. El pipeline también se encarga de invocar al `Reporter` al finalizar para generar métricas y gráficos.

### Clase abstracta EncoderDecoder (pipeline.py)

Todos los módulos (File, Source, Modulation, Channel, ChannelCoding) implementan la misma interfaz ABC con `encode()` y `decode()`. Esto garantiza un contrato uniforme y permite que el Pipeline los trate de forma polimórfica sin conocer sus detalles internos.

### Reporter con patrón Strategy (report.py)

Se implementaron 3 variantes de `Reporter`:
- **ReporterTerminal**: imprime en consola, genera CSV, markdown de métricas y gráficos PNG.
- **ReporterAnalysis**: solo imprime en consola (para el modo análisis donde no se necesitan archivos intermedios).
- **EmptyReporter**: no hace nada (para tests y ejecuciones silenciosas).

Esto desacopla completamente la lógica de cada módulo del formato de salida, permitiendo reutilizar los mismos módulos en diferentes contextos.

### Procesamiento por batch en demodulación (modulation.py:111)

La demodulación calcula distancias euclídeas de forma vectorizada (`self.symbols[:,None,:] - batch[None,:,:]`), pero para evitar problemas de memoria con vectores muy grandes, se procesan en batches de 5000 símbolos. Esto balancea velocidad (operaciones vectorizadas con numpy) con consumo de memoria.

### Generador de patrones de error NumberGenerator (cod_channel.py:161-185)

Para construir la tabla de síndromes, se necesitan todos los patrones de error posibles ordenados por peso (cantidad de bits en error). En vez de generar los 2^n patrones y ordenarlos, se usa un generador que itera combinaciones con `itertools.combinations`, generando primero los de 1 bit, luego 2 bits, etc. Esto es mucho más eficiente para códigos con n grande.

### Análisis adaptativo de errores (analysis.py:247-258)

Al simular BER/SER, si la cantidad de errores detectados es menor a `MIN_ERROR_COUNT=100`, el sistema automáticamente duplica la cantidad de bits simulados (usando slices progresivos del texto codificado). Esto mejora la confianza estadística de las mediciones en SNRs altos donde los errores son raros, sin desperdiciar tiempo en SNRs bajos donde abundan los errores.

### CLI modular (cli.py)

Se ofrecen 5 modos de ejecución desde la línea de comandos:
- `--dry-run`: copia el archivo sin procesar (validar I/O).
- `--huffman-only`: solo codificación/decodificación de fuente.
- `--without-code`: pipeline completo sin codificación de canal.
- `--analyze-system`: módulo F de análisis (BER/SER vs Eb/N0).
- Sin flags: pipeline completo con codificación de canal.

### Codificación Gray por XOR (modulation.py:57)

La conversión binario a Gray se realiza con una sola operación: `n ^ (n >> 1)`. Esto es más eficiente y elegante que una tabla de lookup o conversiones manuales.

### RNG seedeable (channel.py:8-11)

El canal acepta un `rng` (generador de números aleatorios de numpy) opcional. Esto permite fijar la semilla para reproducir exactamente los mismos resultados, lo cual es fundamental para debugging y para los tests unitarios.

### Operaciones vectorizadas con numpy

En lugar de iterar símbolo por símbolo para calcular distancias en la demodulación, se usa broadcasting de numpy para computar todas las distancias en una sola operación matricial. Lo mismo aplica para la aplicación de ruido AWGN y fading en el canal.

### Type hints y aliases (source.py:11-14)

Se definen type aliases (`Bit`, `Code`, `EncDict`, `DecDict`) que documentan la intención del código y facilitan el mantenimiento sin agregar complejidad.

---

## Mejoras a nivel resultados

### Constelaciones teóricas y con datos

Se generan dos gráficos por cada configuración de modulación:
1. **Constelación teórica**: muestra los símbolos ideales, etiquetas Gray y fronteras de decisión.
2. **Constelación con datos**: superpone los símbolos recibidos (con ruido) coloreados por símbolo original, permitiendo visualizar el efecto del canal AWGN.

### Curvas teóricas vs simuladas superpuestas

Los gráficos de Pe y Pb vs Eb/N0 muestran simultáneamente las curvas teóricas (líneas punteadas) y los puntos simulados (markers), facilitando la validación visual de la simulación contra la teoría.

### Comparaciones PSK vs FSK

Para cada valor de M (2, 4, 8, 16), se genera un gráfico comparativo entre PSK y FSK mostrando tanto Pe como Pb. Esto permite visualizar directamente el trade-off entre eficiencia en ancho de banda (PSK) y eficiencia en energía (FSK).

### Análisis con/sin codificación de canal

Se generan gráficos que comparan Pe_sim y Pb_sim con y sin el código lineal de bloques [15,5], mostrando la ganancia de codificación para cada combinación de modulación y M.

### Exportación de datos en CSV

Los resultados de cada simulación se exportan a CSV (`analysis_results_*.csv`), permitiendo post-procesamiento externo (Excel, pandas, etc.) sin tener que re-ejecutar las simulaciones.

### Reporte markdown automático

El sistema genera automáticamente un archivo `metricas.md` con todas las métricas organizadas por módulo: entropía H, longitud promedio L̄, eficiencia η, energías de símbolo/bit, probabilidades de error, y referencias a los gráficos generados.

### Tabla de Huffman completa

Se exporta una tabla CSV (`tabla_huffman.csv`) con columnas: carácter, probabilidad, código Huffman, longitud del código y representación ASCII. Los caracteres de control se representan de forma legible (\\n, \\t, ␠).
