# CÓDIGO PARA LA SIMULACIÓN DEL ALGORITMO DE SHOR
# Este código forma parte de un anexo adicional del Trabajo de Fin de Grado para la obtención del Doble Grado en Física y Matemáticas de nombre
# "Teoría de la Información Cuántica y la Computación Cuántica", de código FT37 del curso 2026. El tutor es Miguel Ángel Martín-Delgado Alcántara.
# El autor de este código, así como del Trabajo de Fin de Grado al que pertence, es Álvaro Mandado Díaz.

# Este código incluye la simulación del algoritmo de Shor necesaria para la comparación de los casos clásico y cuántico en el TFG. Se irá comentando qué hace cada parte del mismo.

# Lo primero es importar los paquetes a utilizar.

import matplotlib.pyplot as plt    # Necesario para dibujar las gráficas
import numpy as np    # Este paquete y el siguiente añaden operaciones matemáticas a Python
import math

np.random.seed(0)   # De esta forma el resultado de las simulaciones es reproducible

# Lo siguiente es definir una clase opaca dentro de la cuál se generarán las simulaciones clásicas y los circuitos cuánticos

class OraculoCompartido:
    def __init__(self, n):
        self.n = n
        if n <= 44:    # Por debajo de ese tamaño se simulará, por encima se usará la fórmula teórica
            self.N = self._generar_semiprimo(n)    # Esta función genera un número semiprimo
        else:
            self.N = 2**n

    def _es_primo(self, num):    # Comprobación por fuerza bruta sobre si un entero es primo o compuesto
        if num < 2: return False
        for i in range(2, int(math.isqrt(num)) + 1):
            if num % i == 0: return False
        return True

    def _generar_semiprimo(self, bits):    # Esta función genera un número semiprimo N=p*q
        bits_p = bits // 2    # El tamaño de uno de los factores
        bits_q = bits - bits_p    # El tamaño del otro factor
        p = np.random.randint(2**(bits_p-1), 2**bits_p - 1)    # Se elige un número aleatorio de 'bits_p' bits y se modifica hasta que se encuentre uno primo (siempre hay alguno entre 2^(n-1) y 2^n-1)
        while not self._es_primo(p): p += 1
        q = np.random.randint(2**(bits_q-1), 2**bits_q - 1)    # Mismo procedimiento
        while not self._es_primo(q) or q == p: q += 1
        return p * q

    def query_clasico_tentativa(self):    # Esta función hace la división tentativa o 'por fuerza bruta'
        if self.n > 44: return np.nan    # No actúa por encima del límite de la simulación
        
        intentos = 0
        limite = int(math.isqrt(self.N))    # Solo prueba hasta la raiz de N
        for i in range(2, limite + 1):
            intentos += 1
            if self.N % i == 0: break    # Corta el bucle cuando encuentra un factor
        return intentos * (self.n**2)    # El coste real es el número de intentos por el número de operaciones por el número de bits (coste clásico total)

    def query_clasico_rho(self):    # Esta función usa el algoritmo rho de Pollard
        if self.n > 44: return np.nan    # No actúa por encima del límite de la simulación
        
        intentos = 0
        if self.N % 2 == 0: return 1 * (self.n**2)    # El algoritmo se puede encontrar en la bibliografía
        x = 2; y = 2; d = 1
        f = lambda x: (x**2 + 1) % self.N
        
        while d == 1:
            intentos += 1
            x = f(x)
            y = f(f(y))
            d = math.gcd(abs(x - y), self.N)
            if intentos > math.isqrt(self.N): break    # Si tarda más que la división tentativa se descarta, aunque el peor caso real es incluso más pequeño (raiz cuarta de N)
            
        return intentos * (self.n**2)

    def curvas_teoricas(self):    # Esta función calcula las curvas teóricas
        coste_op = self.n**2    # Coste de cada operación, que multiplica a la clase de complejidad (esto es, si se tiene O(g(n)) se asume un coste igual a coste_op*g(n))
        N_approx = 2**self.n

        # Peor caso división por fuerza bruta
        l_tent = math.isqrt(N_approx) * coste_op
        
        # Peor caso del algoritmo rho de Pollard
        l_rho = (2**(self.n/4)) * coste_op
        
        # Peor caso de la criba general del cuerpo de números (no simulada)
        ln_N = self.n * math.log(2)
        if ln_N > 1:
            l_gnfs = math.exp(1.9229 * (ln_N**(1/3)) * ((math.log(ln_N))**(2/3))) * coste_op   # Esta fórmula se encuentra en los artículos de la bibliografía
        else:
            l_gnfs = 1 * coste_op    # Caso de 1 qubit
            
        # Profundidad del circuito cuántico de Shor
        l_shor = 72 * (self.n**3)    # El coste según Beckman et al.
        
        return l_tent, l_rho, l_gnfs, l_shor

# Ahora se define la simulación de tamaño 'n'.

def simular_ambos(n):
    oracle = OraculoCompartido(n)
    
    # Simulaciones clásicas
    sim_tent = oracle.query_clasico_tentativa()
    sim_rho = oracle.query_clasico_rho()
    
    # Curvas teóricas
    teo_tent, teo_rho, teo_gnfs, teo_shor = oracle.curvas_teoricas()
    
    return sim_tent, sim_rho, teo_tent, teo_rho, teo_gnfs, teo_shor

# Solo resta simular para distintos tamaños del problema y dibujar los resultados

bits = range(6, 162, 4)    # Los tamaños elegidos

# Listas vacías para guardar los distintos casos
y_sim_tent, y_sim_rho = [], []
y_teo_tent, y_teo_rho, y_teo_gnfs, y_shor = [], [], [], []

for n in bits:    # Se simula para cada posible número de bits 'n'
    s_t, s_r, t_t, t_r, t_g, t_s = simular_ambos(n)
    
    y_sim_tent.append(s_t)
    y_sim_rho.append(s_r)
    y_teo_tent.append(t_t)
    y_teo_rho.append(t_r)
    y_teo_gnfs.append(t_g)
    y_shor.append(t_s)

# Estos mismos resultados se pueden graficar

plt.figure(figsize=(10, 6))

# Curvas teóricas
plt.plot(bits, y_teo_tent, '--', label='División (Peor Caso)', color='darkred', alpha=0.4)
plt.plot(bits, y_teo_rho, '--', label='Pollard Rho (Peor Caso)', color='darkgoldenrod', alpha=0.6)
plt.plot(bits, y_teo_gnfs, 'x--', label='GNFS (Mejor Clásico Límite)', color='green')

# Simulación por debajo de 44 bits
plt.plot(bits, y_sim_tent, 'o', label='División (Simulación)', color='red', alpha=0.5)
plt.plot(bits, y_sim_rho, 'd', label='Pollard Rho (Simulación)', color='orange', alpha=0.8)

# Caso cuántico
plt.plot(bits, y_shor, 's-', label='Shor', color='blue', linewidth=2)

plt.axvline(x=44, color='gray', linestyle=':')

plt.yscale('log')    # Escala logarítmica para apreciar la diferencia exponencial entre el peor caso clásico y el cuántico
plt.xlabel('Número de Bits (n)')
plt.xticks(list(range(10, 170, 10)))
plt.ylabel('Coste (Operaciones / Profundidad)')
plt.title('Comparación de Complejidad: Todos los Métodos Clásicos vs Algoritmo de Shor')
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend(loc='upper left', fontsize='small')
plt.tight_layout()

plt.savefig('shor.png', dpi=300, bbox_inches='tight')
plt.show()