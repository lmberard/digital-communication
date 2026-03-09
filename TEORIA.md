# TEORIA.md — Temas del Trabajo Práctico y de la Materia

## 1. Teoría de la Información

### Entropía de una fuente discreta

La **entropía** mide la cantidad promedio de información (en bits) por símbolo emitido por una fuente:

```
H = -sum( p(x_i) * log2(p(x_i)) )   [bits/símbolo]
```

Propiedades:
- H >= 0 siempre.
- H es máxima cuando todos los símbolos son equiprobables: H_max = log2(k), donde k es el tamaño del alfabeto.
- Ningún código unívocamente decodificable puede tener una longitud promedio menor que H (primer teorema de Shannon para codificación de fuente).

### Primer teorema de Shannon (codificación de fuente)

Para una fuente discreta sin memoria con entropía H, existe un código binario libre de prefijo cuya longitud promedio L̄ satisface:

```
H <= L̄ < H + 1
```

Esto establece que H es el límite inferior alcanzable para la longitud promedio de cualquier código.

---

## 2. Codificación de Fuente — Algoritmo de Huffman

### Descripción

El algoritmo de Huffman construye un **código binario de prefijo óptimo** que minimiza la longitud promedio L̄ para una distribución de probabilidades dada. Es óptimo entre todos los códigos instantáneos (prefijo-libres).

### Procedimiento

1. Crear un nodo hoja por cada símbolo con su probabilidad.
2. Insertar todos los nodos en una cola de prioridad (min-heap).
3. Mientras haya más de un nodo:
   - Extraer los dos nodos de menor probabilidad.
   - Crear un nodo padre con probabilidad = suma de ambos.
   - Asignar bit 0 a la rama izquierda y bit 1 a la derecha.
4. La raíz es el árbol completo; el camino desde la raíz a cada hoja define el código.

### Métricas del código

- **Longitud promedio**: L̄ = sum( p(x_i) * len(code(x_i)) )
- **Eficiencia**: η = H / L̄ (idealmente cercana a 1)
- **Comparación con longitud fija**: un código de longitud fija para k símbolos necesita ceil(log2(k)) bits/símbolo (p.ej., ASCII usa 7-8 bits).

### Propiedades

- Es un código **prefijo** (instantáneo): ninguna palabra código es prefijo de otra, por lo que la decodificación es inmediata sin ambigüedad.
- Es **óptimo**: entre todos los códigos de prefijo, tiene la menor L̄.
- Símbolos más probables reciben códigos más cortos.

---

## 3. Modulación Digital

### Representación vectorial de señales

Toda señal modulada se puede representar como un vector en un espacio de dimensión N, usando una **base ortonormal** de funciones. Para M-PSK con M>=4, N=2 (componentes en fase y cuadratura). Para M-FSK, N=M (una dimensión por frecuencia).

### M-PSK (Phase Shift Keying)

Los M símbolos se ubican en un círculo de radio sqrt(E_s) con fases uniformemente espaciadas:

```
s_i = sqrt(E_s) * [cos(2*pi*i/M), sin(2*pi*i/M)]    para i = 0, ..., M-1
```

Casos particulares:
- **BPSK (M=2)**: dos puntos antipodales en el eje real. Es la modulación más robusta al ruido.
- **QPSK (M=4)**: cuatro puntos a 90 grados. Misma Pb que BPSK pero doble eficiencia espectral.
- **8-PSK, 16-PSK**: más puntos en el círculo, mayor eficiencia espectral pero menor distancia entre símbolos.

PSK es **eficiente en ancho de banda**: al aumentar M, se transmiten más bits/símbolo sin aumentar el ancho de banda, pero se requiere más Eb/N0 para mantener la misma tasa de error.

### M-FSK (Frequency Shift Keying)

Cada símbolo corresponde a una frecuencia diferente. Los símbolos son vectores unitarios en un espacio M-dimensional (matriz identidad escalada):

```
s_i = sqrt(E_s) * e_i    (vector canónico i-ésimo)
```

FSK es **eficiente en energía**: al aumentar M, la probabilidad de error disminuye para el mismo Eb/N0, pero se necesita más ancho de banda (el BW crece linealmente con M).

### Codificación Gray

El **código de Gray** asigna etiquetas binarias a los símbolos de forma que símbolos adyacentes en la constelación difieran en exactamente 1 bit. Esto minimiza la tasa de error de bit (Pb) respecto a la tasa de error de símbolo (Pe), ya que el error más probable (confundir un símbolo con su vecino) solo causa 1 bit erróneo en vez de potencialmente k/2.

Conversión: `gray(n) = n XOR (n >> 1)`

### Energía de símbolo y de bit

- **Energía de símbolo** E_s: energía promedio de los vectores de la constelación.
- **Energía de bit** E_b: E_b = E_s / k, donde k = log2(M) es el número de bits por símbolo.
- En este trabajo se normaliza E_b = 1, por lo que E_s = k.

### Regiones de decisión

El demodulador asigna cada símbolo recibido al símbolo de la constelación más cercano (criterio de **mínima distancia euclídea**, equivalente al detector de máxima verosimilitud para ruido AWGN). Las fronteras de decisión son las mediatrices entre símbolos adyacentes.

---

## 4. Efectos del Canal

### Modelo AWGN (Additive White Gaussian Noise)

El canal AWGN modela el ruido térmico presente en todo sistema de comunicaciones. El ruido es:
- **Aditivo**: se suma a la señal.
- **Blanco**: tiene densidad espectral de potencia plana (afecta todas las frecuencias por igual).
- **Gaussiano**: sus muestras siguen una distribución normal.

```
r = s + n,    donde n ~ N(0, sigma^2)
sigma^2 = N_0 / 2
```

### Relación Eb/N0

La relación **Eb/N0** (energía por bit sobre densidad espectral de ruido) es la métrica fundamental para comparar el rendimiento de diferentes esquemas de modulación:

```
Eb/N0 [dB] = 10 * log10(Eb/N0_lineal)
N_0 = 1 / (Eb/N0_lineal)     (cuando Eb = 1)
```

Un Eb/N0 más alto implica menor potencia de ruido relativa a la señal, y por lo tanto menor probabilidad de error.

### Atenuación / Fading

El canal puede introducir una atenuación multiplicativa que modela el desvanecimiento (fading) de la señal. En este trabajo se usa una atenuación aleatoria con distribución uniforme entre 0.5 y 0.9:

```
r = alpha * s + n,    donde alpha ~ U(0.5, 0.9)
```

---

## 5. Codificación de Canal — Códigos Lineales de Bloques

### Concepto

Los códigos de canal agregan **redundancia controlada** a la secuencia de bits para permitir la **detección y corrección de errores** introducidos por el canal. Un código lineal de bloques (n, k) toma un mensaje de k bits y produce una palabra código de n bits, agregando n-k bits de paridad.

### Código sistemático

En un código **sistemático**, los primeros k bits de la palabra código son el mensaje original, y los últimos n-k bits son la paridad:

```
c = u * G    (mod 2)
```

donde G = [I_k | P] es la **matriz generadora** de dimensión k x n, con I_k la identidad k x k y P la submatriz de paridad.

### Matriz de chequeo de paridad H

A partir de G = [I_k | P], se construye:

```
H = [P^T | I_(n-k)]    de dimensión (n-k) x n
```

Propiedad fundamental: G * H^T = 0 (mod 2), lo que implica que toda palabra código válida c satisface c * H^T = 0.

### Decodificación por síndromes

1. Se calcula el **síndrome** del vector recibido r: s = r * H^T (mod 2).
2. Si s = 0, no hay error detectable.
3. Si s != 0, se busca s en la **tabla de síndromes** para encontrar el patrón de error e más probable.
4. Se corrige: c_corregida = r XOR e.
5. Se extraen los primeros k bits como mensaje decodificado.

### Parámetros del código

- **Distancia mínima** d_min: peso mínimo de Hamming entre dos palabras código distintas. Equivale al peso mínimo de cualquier palabra código no nula.
- **Capacidad de detección**: puede detectar hasta e = d_min - 1 errores.
- **Capacidad de corrección**: puede corregir hasta t = floor((d_min - 1) / 2) errores.
- **Tasa de código**: R = k/n (fracción de bits útiles).

En este trabajo se usa un código [15, 5] con G dada por los docentes.

---

## 6. Análisis de Desempeño del Sistema

### Función Q

La **función Q** es la probabilidad de que una variable aleatoria normal estándar exceda un valor x:

```
Q(x) = (1/2) * erfc(x / sqrt(2))
```

Es la base para calcular las probabilidades de error teóricas.

### Probabilidad de error de símbolo (Pe) - Teórica

**M-PSK:**
```
Pe ≈ 2 * Q( sqrt(2*k*Eb/N0) * sin(pi/M) )    para M >= 4
Pe = Q( sqrt(2*Eb/N0) )                        para M = 2 (BPSK)
```

**M-FSK:**
```
Pe ≈ (M-1) * Q( sqrt(k*Eb/N0) )
```

### Probabilidad de error de bit (Pb) - Teórica

**M-PSK con codificación Gray:**
```
Pb ≈ Pe / k    donde k = log2(M)
```

**M-FSK:**
```
Pb ≈ (M/2) / (M-1) * Pe
```

### Simulación Monte Carlo

Las probabilidades se estiman por simulación:
- Se transmiten N_bits bits a través del sistema completo.
- Se cuentan los errores de bit y de símbolo.
- Pb_sim = errores_bit / total_bits, Pe_sim = errores_símbolo / total_símbolos.
- Para confianza estadística, se requieren al menos ~100 errores por punto de la curva.

### Ganancia de codificación

La **ganancia de codificación** es la reducción en Eb/N0 necesaria para alcanzar una misma tasa de error cuando se usa codificación de canal vs cuando no se usa. Se observa como un desplazamiento horizontal de la curva BER hacia la izquierda.

### Trade-offs fundamentales

| Aspecto | PSK (eficiente en BW) | FSK (eficiente en energía) |
|---|---|---|
| Al aumentar M | Pb empeora | Pb mejora |
| Ancho de banda | Constante | Crece con M |
| Complejidad | Menor (2D) | Mayor (M dimensiones) |
| Aplicación típica | Canales con BW limitado | Canales con potencia limitada |
