# CODE.md — Herramientas y técnicas utilizadas por módulo

## Módulo A — Programa principal, datos y control

**Archivos:** `src/main.py`, `src/file.py`, `src/cli.py`

- **`argparse`** (stdlib): se usa para parsear los argumentos de línea de comandos (--in, --out-prefix, --ebn0, --dry-run, --huffman-only, --analyze-system, --without-code). Permite definir flags, valores por defecto y help automático.
- **`pathlib.Path`** (stdlib): manejo de rutas de archivos para lectura del texto de entrada y escritura del texto recibido. Se usa `Path.read_text()` y `Path.write_text()` para I/O con encoding configurable.
- **Patrón Pipeline** (`pipeline.py`): la clase `Pipeline` recibe una lista de `EncoderDecoder`, ejecuta `encode()` en orden y luego `decode()` en orden inverso. Esto permite componer el sistema como bloques intercambiables: `File -> Source -> [ChannelCoding] -> Modulation -> Channel`.

```python
# Ejemplo: pipeline completo con codificación de canal
pipe = Pipeline([
    File(out_prefix),
    Source(),
    ChannelCoding(n, k, G),
    Modulation(scheme, M),
    Channel(eb_n0_db),
], ReporterTerminal(out_prefix))
path_out = pipe.run(path_in)
```

---

## Módulo B — Codificación y decodificación de fuente (Huffman)

**Archivo:** `src/source.py`

- **`heapq`** (stdlib): se usa como cola de prioridad (min-heap) para construir el árbol de Huffman. Se insertan nodos (probabilidad, id, payload) y se extraen siempre los dos de menor probabilidad. El `id` único evita errores de comparación cuando dos nodos tienen la misma probabilidad.
- **`collections.Counter`** (stdlib): calcula la frecuencia de aparición de cada carácter en el texto en una sola pasada. Se normaliza por el total para obtener probabilidades.
- **Recursión con `_walk()`**: recorre el árbol de Huffman en profundidad (DFS) asignando bit 0 al hijo izquierdo y bit 1 al derecho. Cada hoja genera una entrada en el diccionario `{símbolo: tupla_de_bits}`.
- **`typing`** (stdlib): se definen type aliases (`Bit = int`, `Code = Tuple[Bit, ...]`, `EncDict`, `DecDict`) para documentar los tipos de datos esperados sin overhead en runtime.
- **`numpy.array`** con `dtype=np.uint8`: la salida de encode es un array numpy de bits (0/1), lo que permite operaciones vectorizadas eficientes en los módulos posteriores.
- **Decodificación por buffer**: se acumulan bits en un buffer y se compara contra el diccionario inverso. Se pre-computan las longitudes posibles de código y la longitud máxima para optimizar las comparaciones.

---

## Módulo C — Modulación y demodulación

**Archivo:** `src/modulation.py`

- **`numpy`**: usado extensivamente para:
  - Generar constelaciones PSK con `np.cos()`, `np.sin()` y fases equiespaciadas.
  - Generar constelaciones FSK con `np.eye(M)` (matriz identidad = vectores ortonormales).
  - Calcular distancias euclídeas vectorizadas: `diffs = symbols[:,None,:] - batch[None,:,:]` seguido de `np.sum(diffs**2, axis=2)`. Esto computa todas las distancias M x batch_size en una sola operación.
  - Escalar la constelación: `symbols *= sqrt(k * E_b)` para normalizar la energía.
- **`enum.Enum`**: la clase `Scheme` (FSK, PSK) encapsula los tipos de modulación como enumeración, evitando strings mágicos.
- **`matplotlib.pyplot`**: grafica constelaciones con:
  - `scatter()` para los puntos de la constelación y los datos recibidos.
  - `plot()` para las fronteras de decisión (líneas punteadas entre símbolos).
  - `text()` para las etiquetas Gray de cada símbolo.
  - Figuras de 10x10 pulgadas para buena resolución.
- **`seaborn`**: `sns.color_palette("hls", M)` genera una paleta de M colores distintos para colorear los puntos recibidos según el símbolo original, facilitando la visualización del efecto del ruido.
- **`matplotlib.lines.Line2D`**: se usa para crear entradas de leyenda personalizadas (símbolos, datos, fronteras).
- **Procesamiento por batch**: se procesan 5000 símbolos por batch (`self.batchs = 5000`) para la demodulación, balanceando velocidad de numpy vectorizado con consumo de memoria.
- **Codificación Gray**: `n ^ (n >> 1)` convierte índice binario a índice Gray en una operación.
- **LSB-first**: el mapeo de bits a símbolo se hace con el bit menos significativo primero, consistente en todos los módulos.

---

## Módulo D — Efectos del canal

**Archivo:** `src/channel.py`

- **`numpy.random.default_rng()`**: generador de números aleatorios moderno de numpy (reemplaza al legacy `np.random`). Soporta semillas para reproducibilidad.
  - `rng.normal(0, sigma, shape)`: genera ruido AWGN con la varianza correcta σ² = N₀/2.
  - `rng.uniform(0.5, 0.9, size)`: genera coeficientes de atenuación para fading.
- **Broadcasting de numpy**: la atenuación se aplica como `sym * fades.reshape(-1, 1)`, multiplicando cada fila (símbolo) por su coeficiente de fading sin loops explícitos.
- **Patrón encoder-solo**: el canal solo tiene lógica en `encode()` (aplicar ruido/fading); `decode()` es una identidad (el canal no tiene "decodificador"), ya que la demodulación se encarga de revertir sus efectos.

---

## Módulo E — Codificación de canal

**Archivo:** `src/cod_channel.py`

- **`numpy`** para álgebra matricial módulo 2:
  - Codificación: `(message @ G) % 2` computa u·G mod 2.
  - Síndrome: `(message @ H.T) % 2` computa r·H^T mod 2.
  - Construcción de H: `np.concatenate((P.T, np.eye(n-k)), axis=1)` a partir de G = [I_k | P].
- **`itertools.combinations`**: la clase `NumberGenerator` genera patrones de error de peso creciente. Para peso w, genera todas las C(n,w) combinaciones de posiciones de bit en error. Esto es mucho más eficiente que iterar 2^n patrones cuando n es grande (n=15 en este caso).
- **Código sistemático [15, 5]**: k=5 bits de mensaje, n=15 bits de palabra código, n-k=10 bits de paridad. La matriz G de 5x15 es dada por los docentes y se define en `main.py`.
- **Tabla de síndromes como diccionario**: `{int_síndrome: array_patrón_error}`. El síndrome se convierte a entero con `syndrom @ base` donde `base = [512, 256, 128, ..., 1]` para indexación directa.
- **Cálculo de d_min por fuerza bruta**: itera los 2^k - 1 mensajes no nulos, genera sus palabras código, y encuentra el peso mínimo. Viable porque 2^5 = 32 es pequeño.

---

## Módulo F — Análisis del sistema

**Archivo:** `src/analysis.py`

- **`scipy.special.erfc`**: implementa la función complementaria de error, usada para calcular la función Q: `Q(x) = 0.5 * erfc(x / sqrt(2))`. Esto permite obtener las probabilidades de error teóricas (Pe y Pb) para PSK y FSK.
- **`pandas.DataFrame`**: almacena los resultados de las simulaciones en forma tabular con columnas: M, ebn0_db, theory_bit, theory_symb, sim_bit, sim_symb. Facilita el filtrado, agrupamiento y exportación a CSV.
- **`matplotlib.pyplot`** para gráficos de análisis:
  - `ax.semilogy()`: escala logarítmica en eje Y para visualizar probabilidades que varían en varios órdenes de magnitud.
  - `plt.cm.tab10()`: paleta de colores para distinguir diferentes valores de M.
  - `plt.subplots(1, 2)`: gráficos lado a lado para comparar Pe y Pb en la misma figura.
- **Simulación Monte Carlo**: el sistema completo (source -> [channel_coding] -> modulation -> channel -> demodulation -> [channel_decoding]) se ejecuta para cada combinación de {esquema, M, Eb/N0}, y se cuentan errores de bit y símbolo.
- **Incremento adaptativo de muestras** (`analysis.py:247-258`): si se detectan menos de 100 errores, se duplica la cantidad de bits simulados usando slices progresivos del texto codificado. Esto asegura confianza estadística sin simular innecesariamente muchos bits en regiones de alto error.

---

## Infraestructura transversal

### Pipeline (pipeline.py)

- **Patrón de diseño**: Chain of Responsibility / Pipeline. Cada etapa es un eslabón que transforma datos y se apila para la decodificación inversa.
- **ABC `EncoderDecoder`**: clase abstracta base con métodos `encode()` y `decode()`. Python `abc.ABC` fuerza la implementación en cada módulo.

### Reporter (report.py)

- **Patrón Strategy**: la interfaz `Reporter` (ABC) define 4 métodos (`report_results`, `append_metrics`, `append_line`, `graph`), y cada implementación decide cómo manejar la salida.
- **`csv` manual**: se genera CSV con `f.write(",".join(...))` directamente, sin dependencia de la librería `csv`.
- **`matplotlib.pyplot.savefig()`**: los gráficos se guardan como PNG con `dpi=150` y `bbox_inches="tight"`.

### Testing (tests/)

- **`pytest`**: framework de testing usado para los unit tests.
- **`pytest.fixture`**: se usa para crear instancias de Reporter reutilizables entre tests.
- **`numpy.testing.assert_array_equal`**: comparación exacta de arrays para validar encode/decode roundtrip.
- **`np.allclose`**: comparación con tolerancia para valores flotantes (varianza del ruido, fading).

### Dependencias (requirements.txt)

| Paquete | Versión | Uso |
|---|---|---|
| `numpy` | >=1.26 | Álgebra vectorial, arrays, RNG |
| `scipy` | - | Función erfc para cálculos teóricos |
| `matplotlib` | >=3.8 | Gráficos de constelaciones y curvas de error |
| `seaborn` | >=0.13.2 | Paleta de colores para constelaciones con datos |
| `pandas` | >=2.0 | DataFrames para resultados de análisis |
| `huffman` | 0.1.2 | Comparación con implementación externa (no usado en el pipeline principal) |
