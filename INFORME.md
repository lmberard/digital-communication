# Informe Técnico – TA137 Taller de Comunicaciones Digitales
## Simulación y Análisis de un Sistema de Comunicaciones Digitales

**Autores:** Berard, Lucia Magdalena (101213) · Stejman Peterburg, Julián (102840)
**1er cuatrimestre 2026**

---

## Índice

1. [Módulo A – Estructura del sistema (Pipeline)](#módulo-a--estructura-del-sistema-pipeline)
2. [Módulo B – Codificación de fuente (Huffman)](#módulo-b--codificación-de-fuente-huffman)
3. [Módulo C – Modulación y demodulación (PSK / FSK)](#módulo-c--modulación-y-demodulación-psk--fsk)
4. [Módulo D – Efectos del canal (AWGN)](#módulo-d--efectos-del-canal-awgn)
5. [Módulo E – Codificación de canal (Código lineal de bloques)](#módulo-e--codificación-de-canal-código-lineal-de-bloques)
6. [Módulo F – Análisis del sistema (BER/SER vs Eb/N0)](#módulo-f--análisis-del-sistema-berser-vs-ebn0)

---

## Módulo A – Estructura del sistema (Pipeline)

### Temas de la materia aplicados
- **Diagrama de bloques de un sistema de comunicaciones**: Transmisor → Canal → Receptor, con cada bloque como etapa independiente.
- **Flujo de señal end-to-end**: codificador de fuente → codificador de canal → modulador → canal → demodulador → decodificador de canal → decodificador de fuente.

### Código utilizado

El orquestador del sistema está en `src/pipeline.py` y `src/main.py`.

```python
# src/pipeline.py – La clase Pipeline implementa el patrón Chain of Responsibility
class Pipeline:
    def run(self, input: Input):
        decoders = []
        for process in self.processes:
            decoders.insert(0, process)
            input = process.encode(input, self.reporter)  # encode: izquierda → derecha
        for process in decoders:
            input = process.decode(input, self.reporter)  # decode: derecha → izquierda
        self.reporter.show()
        return input
```

La clase abstracta `EncoderDecoder` define la interfaz que todos los módulos deben implementar:
```python
# src/pipeline.py
class EncoderDecoder(ABC):
    @abstractmethod
    def encode(self, data, reporter) -> Output: pass
    @abstractmethod
    def decode(self, data, reporter) -> Output: pass
```

En `src/main.py` se construye el pipeline completo:
```python
# src/main.py – modo completo con codificación de canal
pipe = pipeline.Pipeline([
    file.File(out_prefix),
    source.Source(),
    cod_channel.ChannelCoding(n=n, k=k, matriz_generadora=matriz_g),
    modulation.Modulation(scheme=scheme, M=M, scale_energy=k/n),
    channel.Channel(eb_n0_db=eb_no_db),
], report.ReporterTerminal(out_prefix))
```

### Explicación teórica

El diagrama de bloques de un sistema de comunicaciones digitales completo tiene la forma:

```
Fuente → [Cod. Fuente] → [Cod. Canal] → [Modulador] → [Canal] → [Demodulador] → [Dec. Canal] → [Dec. Fuente] → Destino
```

- **Codificador de fuente**: elimina redundancia natural del mensaje para reducir la tasa de transmisión.
- **Codificador de canal**: agrega redundancia *controlada* para detectar y corregir errores introducidos por el canal.
- **Modulador**: adapta la señal digital al medio físico de transmisión.
- **Canal**: introduce ruido, atenuación y distorsión.
- **Demodulador/Decodificadores**: proceso inverso para recuperar el mensaje original.

El patrón Pipeline implementado refleja esta estructura exactamente: los `encode()` se llaman en orden secuencial (transmisor) y los `decode()` se llaman en orden inverso (receptor), que es el comportamiento correcto para una cadena de codificadores anidados.

### Análisis de resultados

**¿Tiene sentido?** Sí. El patrón refleja fielmente la arquitectura del sistema de comunicaciones. La simetría encode/decode es correcta: cada módulo sabe cómo deshacer su propia transformación.

**¿Se puede mejorar?**
- El `Pipeline.run()` no maneja excepciones entre etapas. Si un módulo falla (por ejemplo, demodulación recibe un array vacío), el error se propaga sin contexto de en qué etapa ocurrió.
- El patrón podría extenderse para soportar múltiples canales paralelos o procesamiento por bloques sin cargar todo el texto en memoria.

---

## Módulo B – Codificación de fuente (Huffman)

### Temas de la materia aplicados
- **Teoría de la información**: entropía de la fuente H(S), primer teorema de Shannon.
- **Codificación de fuente**: algoritmo de Huffman, código prefijo, código unívocamente decodificable.
- **Estimación de probabilidades**: método de Monte Carlo para estimar P(S=s) a partir de frecuencias relativas.
- **Eficiencia del código**: η = H(S)/L̄ y condición de código quasi-absolutamente óptimo.

### Código utilizado

**Estimación de probabilidades** (`src/source.py:172-184`):
```python
def _symbol_probs(text: str) -> Dict[str, float]:
    cnt = Counter(text)           # ocurrencias de cada símbolo
    n = sum(cnt.values()) or 1
    return {ch: c / n for ch, c in cnt.items()}
    # P(S=s) ≈ (1/n) * Σ 1{c_i = s}   →   estimación Monte Carlo
```

**Construcción del árbol de Huffman** (`src/source.py:190-221`):
```python
def _build_huffman_tree(probs):
    q = [(p, i, ch) for i, (ch, p) in enumerate(probs.items())]
    heapq.heapify(q)   # heap de mínimos
    while len(q) > 1:
        p1, _, n1 = heapq.heappop(q)  # extraer los dos de menor probabilidad
        p2, _, n2 = heapq.heappop(q)
        heapq.heappush(q, (p1 + p2, uid, (n1, n2)))  # combinar en nodo interno
    return q[0][2]
```

**Cálculo de entropía y longitud promedio** (`src/source.py:154-152`):
```python
def entropy(self) -> float:
    return -sum(p * log2(p) for p in self.probs.values() if p > 0)
    # H(S) = -Σ p_k * log2(p_k)

def avg_code_length(self) -> float:
    return sum(p * len(self.encoder[ch]) for ch, p in self.probs.items())
    # L̄ = Σ p_k * l_k
```

**Decodificación** (`src/source.py:41-78`): usa el diccionario inverso `{código → símbolo}`. Acumula bits en un buffer y lo compara contra los códigos posibles. Al hacer match, emite el carácter y limpia el buffer.

### Explicación teórica

La **entropía** de una fuente discreta con alfabeto S es:

```
H(S) = -Σ p_k * log₂(p_k)   [bits/símbolo]
```

Representa la información media por símbolo. Por el **primer teorema de Shannon**, la longitud mínima promedio de cualquier código unívocamente decodificable es:

```
L̄_min = H(S) / log₂(r)
```

donde r es el tamaño del alfabeto del código (r=2 para binario). Entonces `L̄_min = H(S)`.

El **algoritmo de Huffman** construye iterativamente el código óptimo tomando los dos símbolos de menor probabilidad, creando un nodo interno con probabilidad suma, y reinsertándolo. El resultado es un **código prefijo** (ninguna palabra de código es prefijo de otra), lo que garantiza decodificación unívoca. Huffman logra la menor L̄ posible entre todos los códigos prefijos.

La eficiencia se define como:
```
η = H(S) / L̄   →   η ∈ [0, 1]
```

Como `l_k = -log₂(p_k)` puede no ser entero, en general L̄ > H(S). Huffman garantiza `H(S) ≤ L̄ < H(S) + 1`, lo que se conoce como código **quasi-absolutamente óptimo**.

**Resultado del TP** (texto de prueba ADBADEDBBDD):

| Métrica | Valor |
|---------|-------|
| H(S) | 1.788 bits/símbolo |
| L̄_min | 1.788 bits/símbolo |
| L̄ Huffman | 1.815 bits/símbolo |
| η Huffman | 98.51% |
| η ASCII (7 bits) | 25.54% |

### Análisis de resultados

**¿Tiene sentido?** Sí. La eficiencia del 98.51% es consistente con la teoría: Huffman es el código prefijo óptimo y L̄ está dentro del intervalo teórico [H, H+1). La brecha de 1.49% sobre H se debe a que las longitudes óptimas no-enteras (`l_D = 1.14 bits`, `l_B = 1.88 bits`) se redondean al entero superior. La eficiencia de ASCII (25.54%) confirma que un código de longitud fija es muy ineficiente para esta distribución sesgada.

**¿Se puede mejorar?**
- **Estimación de probabilidades**: con solo 11 caracteres de prueba la estimación es poco representativa (mencionado en el informe). Con un texto real de miles de caracteres, las probabilidades estimadas convergen mejor a las reales.
- **Codificación aritmética**: supera teóricamente a Huffman acercándose arbitrariamente a H(S) sin la restricción de longitudes enteras. Permite L̄ → H(S) para bloques grandes.
- **Fragilidad ante errores de bit**: un error de bit en la secuencia Huffman puede causar una desincronización del decodificador y arrastrar errores en múltiples caracteres subsiguientes. Esto ocurre porque el código es de longitud variable: un bit cambiado puede interpretar un código corto como inicio de uno largo. En el TP esto se menciona explícitamente comparando con ASCII que propaga errores solo a nivel de carácter.

---

## Módulo C – Modulación y demodulación (PSK / FSK)

### Temas de la materia aplicados
- **Representación vectorial de señales**: base ortonormal, diagrama de constelación.
- **Modulación digital en banda pasante**: M-PSK y M-FSK.
- **Código de Gray**: etiquetamiento para minimizar la probabilidad de error de bit.
- **Demodulación por decisión dura (hard decision)**: criterio del vecino más cercano (mínima distancia euclídea).
- **Energía de símbolo y de bit**: relación E_s = k · E_b con k = log₂(M).
- **Probabilidad de error de símbolo y de bit**: Pe, Pb y su relación según el etiquetamiento.

### Código utilizado

**Construcción de la constelación PSK** (`src/modulation.py:40-54`):
```python
# M-PSK: símbolos equiespaciados en el círculo unitario, con escala de energía
phases = 2 * np.pi * np.arange(M) / M
symbols = np.column_stack((np.cos(phases), np.sin(phases)))
# Aplicar código de Gray: símbolo i → posición Gray(i) en la constelación
self.symbols = np.zeros((self.M, self.N))
for i in range(M):
    self.symbols[Modulation._bin_to_gray(i)] += symbols[i]
# Escalar para que E_b = 1 → E_s = k
self.symbols *= np.sqrt(self.k * scale_energy)
```

**Código de Gray** (`src/modulation.py:57-58`):
```python
@staticmethod
def _bin_to_gray(n: int) -> int:
    return n ^ (n >> 1)  # conversión binario → Gray
```

**M-FSK** (`src/modulation.py:36-38`): símbolos como vectores de la base canónica de ℝ^M (ortogonales entre sí):
```python
self.symbols = np.eye(M)   # cada símbolo es un vector unitario en una dimensión distinta
self.N = M
```

**Demodulación: vecino más cercano** (`src/modulation.py:119-125`), procesado en batches de 5000 símbolos:
```python
diffs = self.symbols[:,None,:] - batch[None,:,:]   # (M, batch_len, N)
norms = np.sum(diffs**2, axis=2)                   # distancias euclídeas al cuadrado
nearest = np.argmin(norms, axis=0)                 # símbolo más cercano
```

**Energía estimada** (`src/modulation.py:198-209`):
```python
def _estimated_symbol_energy(self, sym):
    # Parseval: energía de señal = norma al cuadrado de su representación vectorial
    energy_per_symbol = np.linalg.norm(self.symbols, axis=1)**2
    # promedio ponderado según distribución empírica de símbolos transmitidos
    average_energy = sum(count * energy_per_symbol[symbol] / len(sym)
                         for symbol, count in zip(*np.unique(sym, return_counts=True)))
    return average_energy

def _estimated_bit_energy(self, sym):
    return self._estimated_symbol_energy(sym) / self.k  # E_b = E_s / k
```

### Explicación teórica

**M-PSK**: cada símbolo `s_i(t)` difiere en fase:
```
s_i(t) = sqrt(2*E_s/T_s) * cos(2π*f_p*t + φ_i),   φ_i = 2πi/M
```

Proyectando sobre la base `{ψ₀=cos, ψ₁=sin}`:
```
s_i = sqrt(E_s) * [cos(φ_i), -sin(φ_i)]
```

Todos los símbolos tienen la misma energía `E_s = ‖s_i‖²`. La distancia mínima entre vecinos decrece con M (ángulo 2π/M se achica), por lo que la probabilidad de error aumenta con M.

**M-FSK**: cada símbolo tiene una frecuencia distinta. En el espacio de señales, cada símbolo es un vector ortogonal a los demás:
```
s_i = sqrt(E_s) * e_i   (vector canónico de ℝ^M)
```

Todos los pares de símbolos están a la misma distancia, por lo que no hay vecinos más cercanos ni lejanos. No tiene sentido aplicar Gray y se usa etiquetado binario.

**Código de Gray**: en M-PSK, los errores más probables son entre símbolos vecinos (a distancia angular `2π/M`). El código de Gray garantiza que dos símbolos adyacentes difieren en exactamente 1 bit. Por eso, si ocurre un error de símbolo entre vecinos (el caso más probable), solo se equivoca 1 bit de los k bits del símbolo. Esto da la relación:
```
Pb ≈ Pe / log₂(M)   [PSK con Gray]
```

Para FSK (sin Gray):
```
Pb ≈ (M/2) / (M-1) * Pe   [FSK]
```

**Relación E_b y E_s**:
```
E_s = k * E_b   con k = log₂(M)
```

Adoptando `E_b = 1` (convención del TP), `E_s = k`, lo que implica que los símbolos se escalan por `sqrt(k)`.

**Probabilidades de error teóricas** (aproximación vecinos más cercanos):
```
Pe_PSK ≈ 2 * Q(sqrt(2*k*E_b/N0) * sin(π/M))      [implementado en analysis.py:65-66]
Pe_FSK ≈ (M-1) * Q(sqrt(k*E_b/N0))                [implementado en analysis.py:109-110]
```

### Análisis de resultados

**¿Tiene sentido?**
- Las constelaciones generadas son correctas: símbolos equiespaciados en el círculo para PSK, vectores ortogonales para FSK.
- Las energías estimadas coinciden exactamente con las teóricas (E_s=3, E_b=1 para M=8), lo que es esperable porque los símbolos se construyen con la energía teórica exacta.
- El etiquetado con Gray reduce Pb respecto de Pe, como indica la teoría.

**¿Se puede mejorar?**
- **Demodulación soft-decision**: la demodulación implementada es hard-decision (toma la decisión del símbolo más cercano antes de pasar al decodificador de canal). Una demodulación soft-decision pasaría métricas de confianza (LLRs) al decodificador de canal, mejorando significativamente la performance. Es la base de códigos turbo y LDPC.
- **M=2 PSK**: para BPSK el código actual usa `N=1` (representación real unidimensional), lo cual es correcto y más eficiente que la representación 2D.
- **Padding de bits**: el código maneja correctamente el caso donde la cantidad de bits no es múltiplo de k, pero el mecanismo de `added_bits` y el desplazamiento del último símbolo agrega complejidad. Una alternativa es simplemente rellenar siempre antes de modular.

---

## Módulo D – Efectos del canal (AWGN)

### Temas de la materia aplicados
- **Canal AWGN** (Additive White Gaussian Noise): modelo de canal más utilizado en comunicaciones digitales.
- **Relación Eb/N0**: parámetro fundamental que caracteriza la calidad del enlace.
- **Varianza del ruido**: relación entre N₀ y σ² para ruido gaussiano complejo.
- **Atenuación (fading)**: efecto del canal que reduce la energía de la señal.

### Código utilizado

Todo el módulo D está en `src/channel.py`:

```python
def encode(self, sym: np.ndarray, reporter: Reporter) -> np.ndarray:
    # Fading opcional (atenuación uniforme por símbolo)
    if self.with_fading:
        fades = rng.uniform(0.5, 0.9, size=num_sym)
        sym = sym * fades.reshape(-1, *(1,) * (sym.ndim - 1))

    # AWGN: convertir Eb/N0 en dB a σ (desviación estándar del ruido)
    ebn0_lin = 10**(self.eb_n0_db / 10)   # dB → lineal
    N0 = 1 / ebn0_lin                      # Eb = 1 por convención → N0 = 1/SNR
    sigma = np.sqrt(N0 / 2)               # σ² = N0/2 por dimensión

    noise = rng.normal(0, sigma, sym.shape)
    return sym + noise                     # adición del ruido

def decode(self, sym, reporter):
    return sym  # el canal no deshace nada: la demodulación está en Módulo C
```

### Explicación teórica

El **canal AWGN** modela el ruido térmico que afecta a toda señal transmitida. La señal recibida es:
```
r(t) = s_i(t) + n(t)
```

donde `n(t)` es ruido gaussiano blanco de densidad espectral de potencia N₀/2 en cada dimensión. En la representación vectorial, el ruido en cada componente tiene varianza:
```
σ² = N₀/2
```

La relación señal a ruido se parametriza como **Eb/N0** (energía por bit sobre densidad espectral de ruido). Adoptando `E_b = 1`:
```
N₀ = E_b / (E_b/N₀) = 1 / SNR_lineal
σ = sqrt(N₀/2) = sqrt(1 / (2 * SNR_lineal))
```

Este es exactamente el cálculo en `channel.py:26-28`. Variar Eb/N0 (manteniendo Eb fija) equivale a variar N₀, es decir, cambiar la potencia del ruido.

La **atenuación** reduce la energía del símbolo recibido. En el código se modela como un factor uniforme en [0.5, 0.9] por símbolo. Esto acerca los símbolos al origen en la constelación, reduciendo la distancia efectiva y aumentando Pe.

### Análisis de resultados

**¿Tiene sentido?** Sí. El cálculo de σ es correcto dado E_b=1. Para Eb/N0=6 dB, σ = sqrt(1/(2·10^0.6)) ≈ 0.316, lo que coincide con lo reportado por el sistema en la consola.

**¿Se puede mejorar?**
- **Modelo de fading**: el fading implementado es una atenuación uniforme determinística por símbolo (U[0.5, 0.9]). Un modelo físicamente más realista sería **fading Rayleigh** (para canales sin línea de visión directa) o **Rician** (con línea de visión), donde la atenuación sigue una distribución estadística determinada por el entorno. El fading Rayleigh eleva la curva BER de forma característica, requiriendo técnicas como diversidad de antenas o OFDM para contrarrestarlo.
- **ISI (Interferencia Intersimbólica)**: no está implementada. En canales con memoria (canal con eco, canal multipropagación), símbolos consecutivos se interfieren entre sí. El canal AWGN puro asume que el canal no tiene memoria. Modelar ISI requeriría un filtro FIR y un ecualizador en el receptor.
- **Ruido en fases**: el ruido en PSK afecta principalmente a la fase, no a la amplitud. El modelo AWGN vectorial implementado es equivalente a ruido independiente en cada cuadratura, lo cual es correcto.

---

## Módulo E – Codificación de canal (Código lineal de bloques)

### Temas de la materia aplicados
- **Códigos lineales de bloques (n,k)**: codificación sistemática mediante matriz generadora G.
- **Matriz de control de paridad H**: verificación de validez de palabras de código.
- **Tabla de síndromes**: decodificación por corrección de errores.
- **Distancia mínima d_min**: parámetro que determina la capacidad de detección y corrección.
- **Peso de Hamming**: métrica sobre palabras de código binarias.

### Código utilizado

**Codificación** (`src/cod_channel.py:37-39`):
```python
for i, message in enumerate(np.split(bits, num_blocks)):
    # u = m · G  (mod 2)   →   palabra de código de n bits a partir de k bits de mensaje
    new_bits[i*self.n:(i+1)*self.n] += (message @ self.G) % 2
```

**Generación de H** (`src/cod_channel.py:111-116`):
```python
def generar_matriz_H(self):
    # G = [I_k | P]   →   H = [P^T | I_{n-k}]
    P = self.G[:, self.k:]     # submatriz de paridad
    return np.concatenate((P.T, np.eye(self.n - self.k)), axis=1).astype(int)
    # Cumple G · H^T = 0 (mod 2)
```

**Tabla de síndromes** (`src/cod_channel.py:118-136`): se generan errores en orden creciente de peso de Hamming (1 bit, 2 bits, ...) y se mapea cada uno a su síndrome `e · H^T`:
```python
def tabla_sindromes(self, H):
    table = {0: np.zeros(self.n)}  # síndrome nulo → sin error
    for e in NumberGenerator(self.n):   # genera errores por peso (combinaciones)
        syndrom = (e @ H.T) % 2
        num = int(syndrom @ self.base)  # síndrome a entero
        if num not in table:
            table[num] = e
        if len(table) >= 2**(self.n - self.k):
            break
    return table
```

**Decodificación** (`src/cod_channel.py:80-99`):
```python
for i, message in enumerate(np.split(bits, num_blocks)):
    syndrom = (message @ self.H.T) % 2    # s = r · H^T
    num = int(syndrom @ self.base)
    e = self.table[num]                   # buscar error en tabla
    message = message ^ e                 # corregir: r ⊕ ê
    new_bits[i*self.k:(i+1)*self.k] += message[:self.k]  # quedarse con k bits informativos
```

**Distancia mínima** (`src/cod_channel.py:138-155`):
```python
def dist_minima(self):
    dmin = n + 1
    for num in range(1, 2**k):
        u = np.array([(num >> i) & 1 for i in range(k)])
        codeword = (u @ self.G) % 2
        weight = int(np.count_nonzero(codeword))   # peso de Hamming
        if 0 < weight < dmin:
            dmin = weight
    e = dmin - 1          # errores detectables
    t = (dmin - 1) // 2   # errores corregibles
    return dmin, e, t
```

### Explicación teórica

Un **código lineal de bloques (n,k)** toma mensajes de k bits y los codifica en palabras de n bits. La codificación sistemática usando la matriz generadora G ∈ {0,1}^(k×n) es:
```
u = m · G   (mod 2)
```

La forma sistemática `G = [I_k | P]` garantiza que los primeros k bits de u son los bits originales del mensaje (bits informativos), y los n-k bits restantes son de paridad.

La **matriz de control de paridad** H ∈ {0,1}^((n-k)×n) se construye como `H = [P^T | I_{n-k}]`, y cumple:
```
G · H^T = 0   (mod 2)
```

Esta propiedad es la clave del decodificador: si `r = u + e` (palabra recibida con error e), entonces:
```
s = r · H^T = (u + e) · H^T = u·H^T + e·H^T = 0 + e·H^T = e·H^T
```

El **síndrome** s solo depende del error, no del mensaje. La tabla de síndromes mapea cada síndrome al patrón de error más probable (el de menor peso de Hamming).

Para el código (15,5) del TP:
- `n=15, k=5, n-k=10` bits de paridad → tasa R = k/n = 1/3
- `d_min = 4`
- Errores detectables: `e = d_min - 1 = 3`
- Errores corregibles: `t = ⌊(d_min-1)/2⌋ = 1`

La tabla de síndromes tiene `2^10 = 1024` entradas, lo que permite mapear todos los síndromes posibles.

### Análisis de resultados

**¿Tiene sentido?** Sí. El código (15,5) con d_min=4 puede corregir 1 error por bloque y detectar hasta 3. Los resultados del informe muestran un umbral en Eb/N0 ≈ 6 dB: por encima mejora la BER respecto de sin codificación; por debajo la empeora.

Esto es físicamente correcto:
- **Región de SNR alta** (por encima del umbral): hay pocos errores por bloque (≤1 por palabra de código), el decodificador los corrige correctamente → la codificación ayuda.
- **Región de SNR baja** (por debajo del umbral): hay muchos errores por bloque (>1), el decodificador intenta corregir pero puede equivocarse e introducir errores adicionales en los k bits informativos → la codificación empeora las cosas. Este efecto se denomina **error floor** del decodificador de síndromes.

Además, la codificación tiene un costo: por cada 5 bits de información se transmiten 15, lo que aumenta el ancho de banda en un factor n/k=3. Para mantener la tasa binaria útil constante, la energía por bit codificado se reduce a `E_c = E_b · k/n = E_b/3`.

**¿Se puede mejorar?**
- **Código más potente**: un código (15,5) con t=1 es conservador. Códigos con mayor tasa de corrección (por ej. BCH, Reed-Solomon) o códigos modernos (Turbo, LDPC) pueden corregir múltiples errores por bloque y acercarse al límite de Shannon.
- **Soft-decision decoding**: la tabla de síndromes implementa hard-decision (trabaja sobre bits decididos). Un decodificador de decisión suave (Viterbi, BCJR, BP) usa las métricas de confianza del demodulador y mejora la ganancia de codificación entre 2-3 dB.
- **Decodificación iterativa**: códigos turbo y LDPC usan decodificación iterativa con paso de mensajes entre decodificadores, lograra desempeño muy cercano a la capacidad del canal.

---

## Módulo F – Análisis del sistema (BER/SER vs Eb/N0)

### Temas de la materia aplicados
- **Curvas BER/SER**: caracterización del rendimiento de un sistema de comunicaciones.
- **Función Q**: relación con la probabilidad de error en canales AWGN.
- **Simulación de Monte Carlo**: estimación empírica de probabilidades de error.
- **Eficiencia espectral vs. eficiencia energética**: trade-off entre PSK y FSK.
- **Ganancia de codificación**: mejora en BER por el uso de codificación de canal.
- **Cota de unión de fronteras** (union bound): aproximación de Pe por vecinos más cercanos.

### Código utilizado

**Curvas teóricas** (`src/analysis.py`):
```python
def q_function(x):
    return 0.5 * erfc(x / np.sqrt(2))    # Q(x) = (1/2)*erfc(x/sqrt(2))

# M-PSK (aproximación vecinos más cercanos)
def pe_psk_theoretical(M, ebn0_linear):
    k = log2(M)
    arg = np.sqrt(2 * k * ebn0_linear) * sin(pi / M)
    return (1 if M == 2 else 2) * q_function(arg)
    # Pe ≈ 2*Q(sqrt(2*k*Eb/N0) * sin(π/M))

# M-FSK
def pe_fsk_theoretical(M, ebn0_linear):
    k = log2(M)
    return (M - 1) * q_function(np.sqrt(k * ebn0_linear))
    # Pe ≈ (M-1)*Q(sqrt(k*Eb/N0))

# Pb usando Gray (PSK) y binario (FSK)
def pb_psk_theoretical(M, ebn0_linear):
    return pe_psk_theoretical(M, ebn0_linear) / log2(M)

def pb_fsk_theoretical(M, ebn0_linear):
    return 0.5 * M * pe_fsk_theoretical(M, ebn0_linear) / (M - 1)
```

**Estimación Monte Carlo con muestreo adaptivo** (`src/analysis.py`, función `run_system_analysis`): si se observan menos de 100 errores, se duplica la cantidad de bits procesados para obtener una estimación más confiable:
```python
# Si hay menos de MIN_ERROR_COUNT errores, se toman más muestras (hasta agotar los bits)
bit_ranges = [slice(0, len(complete_encoding) // 2**(i-1)) for i in range(10, 0, -1)]
```

### Explicación teórica

La **función Q** es la probabilidad de que una variable gaussiana estándar supere el valor x:
```
Q(x) = (1/2) * erfc(x/sqrt(2))
```

Es la forma natural de expresar probabilidades de error en canales AWGN porque el ruido es gaussiano.

**Cota de unión de fronteras (union bound)**: la probabilidad de error de símbolo se acota sumando las probabilidades de confundir cada par de símbolos:
```
Pe ≤ Σ_{j≠i} Q(d_{ij} / (2σ))
```

Tomando solo los `<Ne>` vecinos más cercanos (que dominan la suma):
```
Pe ≈ <Ne> * Q(d_min / (2σ))
```

Para M-PSK, `d_min = 2*sqrt(E_s)*sin(π/M)`, y sustituyendo con E_s = k*E_b:
```
Pe_PSK ≈ 2 * Q(sqrt(2*k*E_b/N0) * sin(π/M))
```

Para M-FSK, `d_min = sqrt(2*E_s)` y hay M-1 vecinos equidistantes:
```
Pe_FSK ≈ (M-1) * Q(sqrt(k*E_b/N0))
```

**Trade-off PSK vs. FSK**:
- **M-PSK** usa una sola frecuencia portadora → eficiente en ancho de banda. Al aumentar M, los símbolos se acercan y Pe aumenta → necesita más potencia.
- **M-FSK** usa una frecuencia distinta por símbolo → el ancho de banda crece con M. Al aumentar M, los símbolos se alejan (más ortogonales) y a SNR alta Pe disminuye → eficiente en energía.

El cruce entre PSK y FSK ocurre alrededor de M=4 en el TP: para M≤4 PSK es mejor; para M≥8 FSK es mejor en términos de Pe a alta SNR.

**Efecto de la codificación de canal**: el código (15,5) escala la energía por bit codificado:
```
E_c = E_b * k/n = E_b / 3
```

Por eso, en los gráficos de Pe vs. Eb/N0 con codificación se hace un ajuste del eje de Eb/N0 para reflejar que la energía disponible por bit codificado es menor (−4.77 dB respecto del caso sin codificación).

### Análisis de resultados

**¿Tiene sentido?** Sí, en todos los aspectos:
1. Las curvas simuladas siguen la forma de las teóricas, con coincidencia mayor a SNR alta (donde hay más eventos de error para estimar).
2. En PSK, Pe aumenta con M (regiones de decisión más angostas). En FSK, Pe tiene cruce: para Eb/N0 > ~2 dB, mayor M implica menor Pe.
3. La codificación de canal mejora Pe por encima del umbral de ~6 dB y la empeora por debajo, exactamente como predice la teoría.
4. Las energías estimadas por Monte Carlo coinciden exactamente con las teóricas.

**¿Se puede mejorar?**

**Monte Carlo a baja SNR**: cuando Pe es muy pequeña (Eb/N0 alto, M pequeño), se necesitan muchísimos bits para observar suficientes errores. El código implementa muestreo adaptivo (duplica bits si hay < 100 errores), pero para Pe < 10⁻⁵ sería necesario simular ~10⁷ bits o más. Alternativas:
  - **Importance sampling**: distorsiona la distribución del ruido para generar más errores, luego pondera los resultados. Permite estimar Pe < 10⁻⁸ con muestras razonables.
  - **Análisis semianálítico**: convolucionar la distribución de errores con la constelación directamente.

**Punto de operación del sistema**: el TP usa Eb/N0 = 6 dB por defecto con 8-PSK y código (15,5). Esto está exactamente en el umbral de ganancia de codificación (~6 dB para Pe). Sería interesante evaluar en Eb/N0 = 8-10 dB donde la ganancia de codificación es clara y el texto recibido se recupera sin errores (mostrado en la Tabla 3.1 del TP).

**Ganancia de codificación real**: con d_min=4 y t=1, el código (15,5) ofrece una ganancia de codificación modesta (~1-2 dB según las curvas). Códigos más modernos como LDPC pueden lograr 5-8 dB de ganancia con la misma tasa R=1/3.

---

## Resumen de temas aplicados por módulo

| Módulo | Temas principales |
|--------|-------------------|
| A | Diagrama de bloques, pipeline, patrón de diseño Chain of Responsibility |
| B | Entropía, primer teorema de Shannon, algoritmo de Huffman, código prefijo, estimación Monte Carlo |
| C | Constelación PSK/FSK, representación vectorial, código de Gray, decisión dura, E_s vs E_b |
| D | Canal AWGN, Eb/N0, varianza del ruido, fading uniforme |
| E | Código lineal (n,k), matriz G y H, síndrome, d_min, peso de Hamming, t errores corregibles |
| F | Curvas BER/SER, función Q, cota de unión, Monte Carlo, trade-off PSK vs FSK, ganancia de codificación |
