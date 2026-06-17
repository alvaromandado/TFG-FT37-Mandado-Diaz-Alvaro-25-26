# CODE FOR THE SIMULATION OF GROVER'S ALGORITHM
# This code is part of an additional APPENDIX of the Bachelor's thesis for obtaining the Double Degree in Physics and Mathematics called
# "Quantum Information and Quantum Computation", code FT37 of the year 2026. The tutor is Miguel Ángel Martín-Delgado Alcántara.
# The author of this code, as well as of the Bachelor's thesis to which it belongs, is Álvaro Mandado Díaz.

# This code includes the simulation of Grover's algorithm necessary for the comparison of classical and quantum cases in the Bachelor's thesis. Each part of it will be commented on.

# The first thing to do is to import the packages that will be used.

import matplotlib.pyplot as plt    # Used for plotting the figures
import numpy as np    # This package and the next one add mathematical operations to Python
import math
from qiskit import QuantumCircuit, transpile    # Used for quantum simulation. The first command generates quantum circuits, the second measures their complexity. Must be installed previously.

np.random.seed(0)   # This way the reproducibility of results is guaranteed

# The next step is to define an opaque class within which the classical simulations and quantum circuits will be generated

class SharedOracle:
    def __init__(self, n):    # We define the problem size parameters, N=2^n and the target
        self.n = n
        self.N = 2**n
        self.target = np.random.randint(0, self.N - 1)
        
    def classical_query(self):    # Simulates the classical search
        attempts = 0
        index_list = list(range(self.N))
        np.random.shuffle(index_list)    # Randomly orders the N elements
        
        for i in index_list:
            attempts += 1    # Counts the number of attempts
            if i == self.target:
                return attempts    # Stops when it finds the target
        return attempts

    def f_oracle(self):    # The quantum oracle that marks the target with a -1 phase
        qc = QuantumCircuit(self.n)
        
        target_bin = format(self.target, f'0{self.n}b')[::-1]    # Convert the target to a binary string
        
        # X gates are applied to the 0 bits of the target
        for i, bit in enumerate(target_bin):
            if bit == '0':
                qc.x(i)

        # A -1 phase is applied only on the target (when all values are 1 since 0->1 has been changed where they were not 1)
        if self.n > 1:
            qc.h(self.n-1)
            qc.mcx(list(range(self.n-1)), self.n-1)
            qc.h(self.n-1)
        else:
            qc.z(0) # Trivial case of 1 qubit
            
        # X gates are undone to recover the target
        for i, bit in enumerate(target_bin):
            if bit == '0':
                qc.x(i)
                
        return qc.to_gate(label="Oracle")

    def inversion(self):    # The inversion about the mean oracle, defined in the Grover's algorithm section
        qc = QuantumCircuit(self.n)
        qc.h(range(self.n))
        qc.x(range(self.n))
        
        # Multi-controlled Z gates are placed on each qubit, which is nothing more than applying Hadamard to the first 'n' qubits before and after a generalized Toffoli
        qc.h(self.n-1)
        qc.mcx(list(range(self.n-1)), self.n-1)
        qc.h(self.n-1)
        
        qc.x(range(self.n))
        qc.h(range(self.n))
        return qc.to_gate(label="Diffuser")    # In classical bibliography this operator is also called a diffuser

    def quantum_circuit(self):    # Grover's quantum circuit is built
        iterations = int(math.floor((math.pi / 4) * math.sqrt(self.N)))    # The optimal number of iterations is |_(pi/4)*sqrt(N)_|
        
        qc = QuantumCircuit(self.n, self.n)
        
        qc.h(range(self.n))    # The initial state is prepared to |phi>
        
        oracle = self.f_oracle()    # The gates defined above are used
        inverter = self.inversion()
        
        for _ in range(iterations):    # The necessary iterations are performed
            qc.append(oracle, range(self.n))
            qc.append(inverter, range(self.n))
        
        qc.measure(range(self.n), range(self.n))    # Ultimately the measurement is performed
        
        return qc

# Now the simulation of size 'n' is defined.

def simulate_both(n):
    # Through the class defined above, the oracle for the classical and quantum cases is generated
    oracle = SharedOracle(n)
    
    classical_steps = oracle.classical_query()    # The classical simulation is performed
    
    classical_cost = classical_steps * n
    
    limit_cost = (2**n) * n

    qc = oracle.quantum_circuit()    # The quantum simulation is performed

    qc_transpiled = transpile(qc, optimization_level=1)    # It is necessary to correct the depth by writing the generalized Toffoli gates in terms of simple gates
    quantum_cost = qc_transpiled.depth()
    
    return classical_cost, limit_cost, quantum_cost

# Now it only remains to simulate for different problem sizes and plot the results

bits = range(2, 22)    # The chosen sizes
y_clas, y_lim, y_quant = [], [], []    # Empty lists to store the three cases

for n in bits:    # Simulate for each possible number of bits 'n'
    c, l, q = simulate_both(n)
    y_clas.append(c); y_lim.append(l); y_quant.append(q)

# These same results can be plotted

plt.figure(figsize=(10, 6))

plt.plot(bits, y_clas, 'o-', label='Classical', color='red', alpha=0.5)    # Classical curve
plt.plot(bits, y_lim, 'x--', label='Worst Case', color='green')    # Limit curve (Worst classical case)
plt.plot(bits, y_quant, 's-', label='Grover', color='blue', linewidth=2)    # Quantum curve

plt.yscale('log')    # Logarithmic scale to appreciate the exponential difference between the worst classical case and the quantum case
plt.xlabel('Number of Bits (n)')
plt.xticks(list(bits))
plt.ylabel('Cost (Operations / Depth)')
plt.title('Complexity comparison: Classical vs Grover')
plt.grid(True, which="both", linestyle="--",color='lightgray', alpha=0.5)
plt.legend()
plt.tight_layout()

plt.savefig('grover.png', dpi=300, bbox_inches='tight')
plt.show()