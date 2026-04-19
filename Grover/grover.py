# CÓDIGO PARA LA SIMULACIÓN DEL ALGORITMO DE GROVER
# Este código forma parte de un anexo adicional del Trabajo de Fin de Grado para la obtención del Doble Grado en Física y Matemáticas de nombre
# "Teoría de la Información Cuántica y la Computación Cuántica", de código FT37 del curso 2026. El tutor es Miguel Ángel Martín-Delgado Alcántara.
# El autor de este código, así como del Trabajo de Fin de Grado al que pertence, es Álvaro Mandado Díaz.

# Este código incluye la simulación del algoritmo de Grover necesaria para la comparación de los casos clásico y cuántico en el TFG. Se irá comentando qué hace cada parte del mismo.

# Lo primero es importar los paquetes a utilizar.

import matplotlib.pyplot as plt    # Necesario para dibujar las gráficas
import numpy as np    # Este paquete y el siguiente añaden operaciones matemáticas a Python
import math
from qiskit import QuantumCircuit, transpile    # Para la simulación cuántica. El primer comando genera circuitos cuánticos, el segundo mide su complejidad.  Debe ser instalado previamente

np.random.seed(0)   # De esta forma el resultado de las simulaciones es reproducible

# Lo siguiente es definir una clase opaca dentro de la cuál se generarán las simulaciones clásicas y los circuitos cuánticos

class OraculoCompartido:
    def __init__(self, n):    # Definimos los parámetros de tamaño del problema, N=2^n y el objetivo
        self.n = n
        self.N = 2**n
        self.objetivo = np.random.randint(0, self.N - 1)
        
    def query_clasico(self):    # Simula la búsqueda clásica
        intentos = 0
        lista_indices = list(range(self.N))
        np.random.shuffle(lista_indices)    # Ordena aleatoriamente los N elementos
        
        for i in lista_indices:
            intentos += 1    # Cuenta el número de intentos
            if i == self.objetivo:
                return intentos    # Para cuando encuentra el objetivo
        return intentos

    def oraculo_f(self):    # El oráculo cuántico que marca con fase -1 el objetivo
        qc = QuantumCircuit(self.n)
        
        obj_bin = format(self.objetivo, f'0{self.n}b')[::-1]    # Convertir el objetivo a una cadena binaria
        
        # Se aplican puertas X en los bits 0 del objetivo
        for i, bit in enumerate(obj_bin):
            if bit == '0':
                qc.x(i)

        # Se aplica fase -1 solo sobre el objetivo (cuando todos los valores son 1 ya que se ha cambiado 0->1 allá donde no eran 1)
        if self.n > 1:
            qc.h(self.n-1)
            qc.mcx(list(range(self.n-1)), self.n-1)
            qc.h(self.n-1)
        else:
            qc.z(0) # Caso trivial de 1 qubit
            
        # Se deshacen las puertas X para recuperar el objetivo
        for i, bit in enumerate(obj_bin):
            if bit == '0':
                qc.x(i)
                
        return qc.to_gate(label="Oráculo")

    def inversion(self):    # El oráculo de inversión sobre la media, definido en la sección del algoritmo de Grover
        qc = QuantumCircuit(self.n)
        qc.h(range(self.n))
        qc.x(range(self.n))
        
        # Se colocan puertas multicontroladas Z en cada qubit, que no es más que aplicar Hadamard en los primeros 'n' qubits antes y después de una Toffoli generalizada
        qc.h(self.n-1)
        qc.mcx(list(range(self.n-1)), self.n-1)
        qc.h(self.n-1)
        
        qc.x(range(self.n))
        qc.h(range(self.n))
        return qc.to_gate(label="Difusor")    # En bibliografía clásica a este operador también se le llama difusor

    def circuito_cuantico(self):    # Se construye el circuito cuántico de Grover
        iteraciones = int(math.floor((math.pi / 4) * math.sqrt(self.N)))    # El número óptimo de iteraciones es |_(pi/4)*sqrt(N)_|
        
        qc = QuantumCircuit(self.n, self.n)
        
        qc.h(range(self.n))    # Se prepara el estado inicial a |phi>
        
        oraculo = self.oraculo_f()    # Se utilizan las puertas definidas arriba
        inversor = self.inversion()
        
        for _ in range(iteraciones):    # Se realizan las iteraciones necesarias
            qc.append(oraculo, range(self.n))
            qc.append(inversor, range(self.n))
        
        qc.measure(range(self.n), range(self.n))    # En última instancia se realiza la medida
        
        return qc

# Ahora se define la simulación de tamaño 'n'.

def simular_ambos(n):
    # Mediante la clase definida arriba se genera el oráculo para el caso clásico y el cuántico
    oracle = OraculoCompartido(n)
    
    pasos_clasicos = oracle.query_clasico()    # Se hace la simulación clásica
    
    coste_clasico = pasos_clasicos * n
    
    coste_limite = (2**n) * n

    qc = oracle.circuito_cuantico()    # Se hace la simulación cuántica

    qc_transpiled = transpile(qc, optimization_level=1)    # Es necesario corregir la profundidad escribiendo las puertas Toffoli generalizadas en función de puertas simples
    coste_cuantico = qc_transpiled.depth()
    
    return coste_clasico, coste_limite, coste_cuantico

# Solo resta simular para distintos tamaños del problema y dibujar los resultados

bits = range(2, 22)    # Los tamaños elegidos
y_clas, y_lim, y_quant = [], [], []    # Listas vacías para guardar los tres casos

for n in bits:    # Se simula para cada posible número de bits 'n'
    c, l, q = simular_ambos(n)
    y_clas.append(c); y_lim.append(l); y_quant.append(q)

# Estos mismos resultados se pueden graficar

plt.figure(figsize=(10, 6))

plt.plot(bits, y_clas, 'o-', label='Clásico', color='red', alpha=0.5)    # Curva clásica
plt.plot(bits, y_lim, 'x--', label='Clásico (Peor Caso)', color='green')    # Curva límite
plt.plot(bits, y_quant, 's-', label='Grover', color='blue', linewidth=2)    # Curva cuántica

plt.yscale('log')    # Escala logarítmica para apreciar la diferencia exponencial entre el peor caso clásico y el cuántico
plt.xlabel('Número de Bits (n)')
plt.xticks(list(bits))
plt.ylabel('Coste (Operaciones / Profundidad)')
plt.title('Comparación de Complejidad: Búsqueda Clásica vs Grover')
plt.grid(True, which="both", linestyle="--",color='lightgray', alpha=0.5)
plt.legend()
plt.tight_layout()

plt.savefig('grover.png', dpi=300, bbox_inches='tight')
plt.show()