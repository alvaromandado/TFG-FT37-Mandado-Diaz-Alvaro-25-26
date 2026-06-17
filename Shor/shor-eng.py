# CODE FOR THE SIMULATION OF SHOR'S ALGORITHM
# This code is part of an additional APPENDIX of the Bachelor's thesis for obtaining the Double Degree in Physics and Mathematics called
# "Quantum Information and Quantum Computation", code FT37 of the year 2026. The tutor is Miguel Ángel Martín-Delgado Alcántara.
# The author of this code, as well as of the Bachelor's thesis to which it belongs, is Álvaro Mandado Díaz.

# This code includes the simulation of Shor's algorithm necessary for the comparison of classical and quantum cases in the Bachelor's thesis. Each part of it will be commented on.

# The first thing to do is to import the packages that will be used.

import matplotlib.pyplot as plt    # Used for plotting the figures
import numpy as np    # This package and the next one add mathematical operations to Python
import math

np.random.seed(0)   # This way the reproducibility of results is guaranteed

# The next step is to define an opaque class within which the classical simulations and quantum circuits will be generated

class SharedOracle:
    def __init__(self, n):
        self.n = n
        if n <= 44:    # Below this size it will be simulated, above it the theoretical formula will be used
            self.N = self._generate_semiprime(n)    # This function generates a semiprime number
        else:
            self.N = 2**n

    def _is_prime(self, num):    # Brute-force check on whether an integer is prime or composite
        if num < 2: return False
        for i in range(2, int(math.isqrt(num)) + 1):
            if num % i == 0: return False
        return True

    def _generate_semiprime(self, bits):    # This function generates a semiprime number N=p*q
        bits_p = bits // 2    # The size of one of the factors
        bits_q = bits - bits_p    # The size of the other factor
        p = np.random.randint(2**(bits_p-1), 2**bits_p - 1)    # A random number of 'bits_p' bits is chosen and modified until a prime is found (there is always one between 2^(n-1) and 2^n-1)
        while not self._is_prime(p): p += 1
        q = np.random.randint(2**(bits_q-1), 2**bits_q - 1)    # Same procedure
        while not self._is_prime(q) or q == p: q += 1
        return p * q

    def classical_query_trial(self):    # This function performs trial division or 'brute force'
        if self.n > 44: return np.nan    # Does not act above the simulation limit
        
        attempts = 0
        limit = int(math.isqrt(self.N))    # Only tests up to the square root of N
        for i in range(2, limit + 1):
            attempts += 1
            if self.N % i == 0: break    # Breaks the loop when it finds a factor
        return attempts * (self.n**2)    # The real cost is the number of attempts times the number of operations times the number of bits (total classical cost)

    def classical_query_rho(self):    # This function uses Pollard's rho algorithm
        if self.n > 44: return np.nan    # Does not act above the simulation limit
        
        attempts = 0
        if self.N % 2 == 0: return 1 * (self.n**2)    # The algorithm can be found in the bibliography
        x = 2; y = 2; d = 1
        f = lambda x: (x**2 + 1) % self.N
        
        while d == 1:
            attempts += 1
            x = f(x)
            y = f(f(y))
            d = math.gcd(abs(x - y), self.N)
            if attempts > math.isqrt(self.N): break    # If it takes longer than trial division it is discarded, although the true worst case is even smaller (fourth root of N)
            
        return attempts * (self.n**2)

    def theoretical_curves(self):    # This function calculates the theoretical curves
        op_cost = self.n**2    # Cost of each operation, which multiplies the complexity class (that is, if we have O(g(n)) a cost equal to op_cost*g(n) is assumed)
        N_approx = 2**self.n

        # Worst case brute-force division
        l_trial = math.isqrt(N_approx) * op_cost
        
        # Worst case of Pollard's rho algorithm
        l_rho = (2**(self.n/4)) * op_cost
        
        # Worst case of the general number field sieve (not simulated)
        ln_N = self.n * math.log(2)
        if ln_N > 1:
            l_gnfs = math.exp(1.9229 * (ln_N**(1/3)) * ((math.log(ln_N))**(2/3))) * op_cost   # This formula is found in the bibliography articles
        else:
            l_gnfs = 1 * op_cost    # 1 qubit case
            
        # Depth of Shor's quantum circuit
        l_shor = 72 * (self.n**3)    # The cost according to Beckman et al.
        
        return l_trial, l_rho, l_gnfs, l_shor

# Now the simulation of size 'n' is defined.

def simulate_both(n):
    oracle = SharedOracle(n)
    
    # Classical simulations
    sim_trial = oracle.classical_query_trial()
    sim_rho = oracle.classical_query_rho()
    
    # Theoretical curves
    theo_trial, theo_rho, theo_gnfs, theo_shor = oracle.theoretical_curves()
    
    return sim_trial, sim_rho, theo_trial, theo_rho, theo_gnfs, theo_shor

# Now it only remains to simulate for different problem sizes and plot the results

bits = range(6, 162, 4)    # The chosen sizes

# Empty lists to store the different cases
y_sim_trial, y_sim_rho = [], []
y_theo_trial, y_theo_rho, y_theo_gnfs, y_shor = [], [], [], []

for n in bits:    # Simulate for each possible number of bits 'n'
    s_t, s_r, t_t, t_r, t_g, t_s = simulate_both(n)
    
    y_sim_trial.append(s_t)
    y_sim_rho.append(s_r)
    y_theo_trial.append(t_t)
    y_theo_rho.append(t_r)
    y_theo_gnfs.append(t_g)
    y_shor.append(t_s)

# These same results can be plotted

plt.figure(figsize=(10, 6))

# Theoretical curves
plt.plot(bits, y_theo_trial, '--', label='Division (Worst Case)', color='darkred', alpha=0.4)
plt.plot(bits, y_theo_rho, '--', label='Pollard Rho (Worst Case)', color='darkgoldenrod', alpha=0.6)
plt.plot(bits, y_theo_gnfs, 'x--', label='GNFS (Best Classical Limit)', color='green')

# Simulation below 44 bits
plt.plot(bits, y_sim_trial, 'o', label='Division (Simulation)', color='red', alpha=0.5)
plt.plot(bits, y_sim_rho, 'd', label='Pollard Rho (Simulation)', color='orange', alpha=0.8)

# Quantum case
plt.plot(bits, y_shor, 's-', label='Shor', color='blue', linewidth=2)

plt.axvline(x=44, color='gray', linestyle=':')

plt.yscale('log')    # Logarithmic scale to appreciate the exponential difference between the worst classical case and the quantum case
plt.xlabel('Number of Bits (n)')
plt.xticks(list(range(10, 170, 10)))
plt.ylabel('Cost (Operations / Depth)')
plt.title('Complexity Comparison: All Classical Methods vs Shor\'s Algorithm')
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend(loc='upper left', fontsize='small')
plt.tight_layout()

plt.savefig('shor.png', dpi=300, bbox_inches='tight')
plt.show()