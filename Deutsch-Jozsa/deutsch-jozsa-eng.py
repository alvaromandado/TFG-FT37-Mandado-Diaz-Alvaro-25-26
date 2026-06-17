# CODE FOR THE SIMULATION OF THE DEUTSCH-JOZSA ALGORITHM
# This code is part of an additional anPPENDIX of the Bachelor's thesis for obtaining the Double Degree in Physics and Mathematics called
# "Quantum Information and Quantum Computation", code FT37 of the year2026. The tutor is Miguel Ángel Martín-Delgado Alcántara.
# The author of this code, as well as of the Bachelor's thesis to which it belongs, is Álvaro Mandado Díaz.

# This code includes the simulation of the Deutsch-Jozsa algorithm necessary for the comparison of classical and quantum cases in the Bachelor's thesis. Each part of it will be commented on.

# The first thing to do is to import the packages that will be used.

import matplotlib.pyplot as plt    # Used for plotting the figures
import numpy as np    # This package is used for generating random numbers and for the manipulation of arrays
from qiskit import QuantumCircuit, transpile   # Used for quantum simulation. The first command generates quantum circuits, the second measures their complexity.

np.random.seed(0)   # This way the reproducibility of results is guaranteed

# The next step is to define a class within which the classical simulations and quantum circuits will be generated

class SharedOracle:
    def __init__(self, n, mode='balanced'):    # It will generate balanced oracles for 'n' bit problems
        self.n = n; self.mode = mode
        if mode == 'constant':    # In case a constant oracle is desired, whose image is a random value between 0 and 1 stored in 'self.val'
            self.val = np.random.choice([0, 1])
            self.b = 0 # No mask
        else:    # Otherwise, a non-zero number less than 2^n-1 is chosen and the balanced function is defined as f(x)=x*b mod 2, where 'b' is the binary string of the chosen number (mask)
            self.b = np.random.randint(1, 2**n - 1)
            self.val = None # It is not applicable if the oracle is not constant

    def classical_query(self, x):   # This function simulates f(x) in the classical case
        if self.mode == 'constant':    # If the oracle was constant, it returns that value 'self.val'
            return self.val
        else:    # If not, it performs a bitwise product between 'x' and 'b' using the AND operator (&) and returns it modulo 2
            return bin(x & self.b).count('1') % 2

    def quantum_circuit(self):    # This function simulates the oracle U_f
        qc = QuantumCircuit(self.n + 1)    # The circuit has the 'n' bits of the input register and the additional qubit, which in the theoretical study would be in the state |->
        if self.mode == 'constant':
            if self.val == 1: qc.x(self.n) # If the oracle is such that f=0, then the output is already 0. If it is f=1, then it needs to be flipped. This will represent the phase kickback
        else:
            b_str = format(self.b, f'0{self.n}b')[::-1]    # Reverses the order of the mask 'b', because Qiskit reads numbers in reverse (from back to front)
            for q, bit in enumerate(b_str):
                if bit == '1': qc.cx(q, self.n)    # For each 1 in the mask, a CNOT gate is placed, which is the way to implement the string product in quantum circuits
        return qc

# Now the simulation of size 'n' is defined

def simulate_both(n):
    # Through the class defined above, the same oracle is generated for the classical and quantum cases (that is, it represents the same function f(x))
    oracle = SharedOracle(n, mode='balanced')

    # In the classical case, the cost is the number of queries multiplied by the size of the problem (you also have to read each of the 'n' bits)
    limit = (2**n // 2) + 1    # The worst classical case
    res = []; consults = 0
    for i in range(limit):    # Classical simulation
        res.append(oracle.classical_query(i))    # A new value is stored in a dummy variable the result of each measurement
        consults += 1    # The number of steps performed is counted
        if len(set(res)) > 1: break   # As it is known that the oracle is balanced, the loop stops when two different values are found in the image (0 and 1)
    classical_cost = consults * n
    worst_case_cost = limit * n

    # In the quantum case, the cost is taken as the depth (of Qiskit) of the circuit
    
    qc = QuantumCircuit(n+1, n)
    qc.x(n); qc.h(range(n+1))    # Preparing the state |phi>|->
    qc.compose(oracle.quantum_circuit(), inplace=True)    # The state prepared is passed through the oracle U_f
    qc.h(range(n)); qc.measure(range(n), range(n))    # To measure, Qiskit does not know how to measure the state |psi>, so it has to pass it through Hadamard gates on each qubit
    quantum_cost = qc.depth()
    
    return classical_cost, worst_case_cost, quantum_cost

# Now it only remains to simulate for different problem sizes and plot the results

bits = range(2, 21)    # The chosen sizes
y_clas, y_lim, y_quant = [], [], []    # Empty lists to store the three cases

for n in bits:    # Simulate for each possible number of bits 'n'
    c, l, q = simulate_both(n)
    y_clas.append(c); y_lim.append(l); y_quant.append(q)

# This results in three lists with the costs of each case, which are plotted below. The classical case is plotted in red, the worst classical case in green, and the quantum case in blue

plt.figure(figsize=(10, 6))

plt.plot(bits, y_clas, 'o-', label='Classical', color='red', alpha=0.5)    # Classical curve
plt.plot(bits, y_lim, 'o-', label='Worst Case', color='green')    # Worst classical case curve
plt.plot(bits, y_quant, 's-', label='Deutsch-Jozsa', color='blue', linewidth=2)    # Quantum curve

plt.yscale('log')    # Logarithmic scale to appreciate the exponential difference between the worst classical case and the quantum case
plt.xlabel('Number of Bits (n)')
plt.xticks(list(bits))
plt.ylabel('Cost (Operations / Depth)')
plt.title('Complexity comparison: Classical vs Deutsch-Jozsa')
plt.grid(True, which="both", linestyle="--",color='lightgray', alpha=0.5)
plt.legend()
plt.tight_layout()

plt.savefig('deutsch-jozsa.png', dpi=300, bbox_inches='tight')
plt.show()