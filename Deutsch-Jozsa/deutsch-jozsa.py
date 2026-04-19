# CÓDIGO PARA LA SIMULACIÓN DEL ALGORITMO DE DEUTSCH-JOZSA
# Este código forma parte de un anexo adicional del Trabajo de Fin de Grado para la obtención del Doble Grado en Física y Matemáticas de nombre
# "Teoría de la Información Cuántica y la Computación Cuántica", de código FT37 del curso 2026. El tutor es Miguel Ángel Martín-Delgado Alcántara.
# El autor de este código, así como del Trabajo de Fin de Grado al que pertence, es Álvaro Mandado Díaz.

# Este código incluye la simulación del algoritmo de Deutsch-Jozsa necesaria para la comparación de los casos clásico y cuántico en el TFG. Se irá comentando qué hace cada parte del mismo.

# Lo primero es importar los paquetes a utilizar.

import matplotlib.pyplot as plt    # Necesario para dibujar las gráficas
import numpy as np    # Este paquete añade operaciones matemáticas a Python
from qiskit import QuantumCircuit, transpile   # Para la simulación cuántica. El primer comando genera circuitos cuánticos, el segundo mide su complejidad. Debe ser instalado previamente

np.random.seed(0)   # De esta forma el resultado de las simulaciones es reproducible

# Lo siguiente es definir una clase opaca dentro de la cuál se generarán las simulaciones clásicas y los circuitos cuánticos

class OraculoCompartido:
    def __init__(self, n, mode='balanceado'):    # De forma genérica generará oráculos balanceados para problemas de 'n' bits
        self.n = n; self.mode = mode
        if mode == 'constante':    # En caso de querer un oráculo constante, cuya imagen sea un valor aleatorio entre 0 y 1 guardado en 'self.val'
            self.val = np.random.choice([0, 1])
            self.b = 0 # No hay máscara
        else:    # En caso contrario, se elige un número no nulo menor a 2^n-1 y se define la función balanceada como f(x)=x*b mod 2, donde 'b' es la cadena binaria del número elegido (máscara)
            self.b = np.random.randint(1, 2**n - 1)
            self.val = None # No aplica si el oráculo no es constante

    def query_clasico(self, x):   # Esta función simula f(x) en el caso clásico
        if self.mode == 'constante':    # Si el oráculo era constante devuelve ese valor 'self.val'
            return self.val
        else:    # Si no hace el producto bit a bit entre 'x' y 'b' mediante el operador AND (&) y lo devuelve módulo 2
            return bin(x & self.b).count('1') % 2

    def circuito_cuantico(self):    # Esta función simula el oráculo U_f
        qc = QuantumCircuit(self.n + 1)    # El circuito tiene los 'n' bits del registro de entrada y el qubit adicional, que en el estudio teórico se encontraría en el estado |->
        if self.mode == 'constante':
            if self.val == 1: qc.x(self.n) # Si el oráculo es tal que f=0, entonces la salida ya es 0. Si es f=1, hay que darle la vuelta. Esto representará el phase kickback
        else:
            b_str = format(self.b, f'0{self.n}b')[::-1]    # Invierte el orden de la máscara 'b', porque Qiskit lee los números al revés (de atrás hacia adelante)
            for q, bit in enumerate(b_str):
                if bit == '1': qc.cx(q, self.n)    # En cada 1 de la máscara se coloca una CNOT, que es la forma de implementar el producto de cadenas en circuitos cuánticos
        return qc

# Ahora se define la simulación de tamaño 'n'.

def simular_ambos(n):
    # Mediante la clase definida arriba se genera el mismo oráculo para el caso clásico y el cuántico (esto es, representa la misma función f(x))
    oraculo = OraculoCompartido(n, mode='balanceado')

    # En el caso clásico el coste es el número de consultas multiplicado por el tamaño del problema (hay que leer también cada uno de los 'n' bits)
    limite = (2**n // 2) + 1    # El peor caso clásico
    res = []; consultas = 0
    for i in range(limite):    # Simulación clásica
        res.append(oraculo.query_clasico(i))    # Se almacena en una variable muda el resultado de cada medida
        consultas += 1    # Se cuenta el número de pasos realizados
        if len(set(res)) > 1: break   # Como se conoce que el oráculo es balanceado, el bucle para a la que se encuentran dos valores distintos en la imgane (0 y 1)
    coste_clasico = consultas * n
    coste_peor = limite * n

    # En el caso cuántico se toma como el coste la profundidad (de Qiskit) del circuito
    qc = QuantumCircuit(n+1, n)
    qc.x(n); qc.h(range(n+1))    # Preparación del estado |phi>|->
    qc.compose(oraculo.circuito_cuantico(), inplace=True)    # Se hace pasar el estado preparado por el oráculo U_f
    qc.h(range(n)); qc.measure(range(n), range(n))    # Para hacer la medida Qiskit no sabe medir el estado |psi>, y tiene que pasarlo por puertas de Hadamard en cada qubit
    coste_cuantico = qc.depth()
    
    return coste_clasico, coste_peor, coste_cuantico

# Solo resta simular para distintos tamaños del problema y dibujar los resultados

bits = range(2, 21)    # Los tamaños elegidos
y_clas, y_lim, y_quant = [], [], []    # Listas vacías para guardar los tres casos

for n in bits:    # Se simula para cada posible número de bits 'n'
    c, l, q = simular_ambos(n)
    y_clas.append(c); y_lim.append(l); y_quant.append(q)

# Estos mismos resultados se pueden graficar

plt.figure(figsize=(10, 6))

plt.plot(bits, y_clas, 'o-', label='Clásico', color='red', alpha=0.5)    # Curva clásica
plt.plot(bits, y_lim, 'o-', label='Clásico (Peor Caso)', color='green')    # Curva límite
plt.plot(bits, y_quant, 's-', label='Deutsch-Jozsa', color='blue', linewidth=2)    # Curva cuántica

plt.yscale('log')    # Escala logarítmica para apreciar la diferencia exponencial entre el peor caso clásico y el cuántico
plt.xlabel('Número de Bits (n)')
plt.xticks(list(bits))
plt.ylabel('Coste (Operaciones / Profundidad)')
plt.title('Comparación de Complejidad: Clásico vs Deutsch-Jozsa')
plt.grid(True, which="both", linestyle="--",color='lightgray', alpha=0.5)
plt.legend()
plt.tight_layout()

plt.savefig('deutsch-jozsa.png', dpi=300, bbox_inches='tight')
plt.show()