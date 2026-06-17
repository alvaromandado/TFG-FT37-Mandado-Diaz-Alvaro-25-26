# Shor's Algorithm

*Read this in other languages: [Español](README.md)*

This branch contains the Deutsch-Jozsa algorithm implementation. This semi-classical algorithm is used to factorize integers.


## Description
Due to the elevated computational complexity, the `shor.py` script calculates the Shor's algorithm circuit's depth, because the implementation, for example, of the Quantum Fourier Transform becomes immesurable even for small integers.


## Contents
* **`shor-eng.py`**: A number of small cases are simulated through the use of brute division and Pollard's rho algorithm, and then the theoretical complexity curves for all of the algorithms at any problem size are drawn.
* **`shor-eng.png`**: Complexity comparison between Shor's algorithm, GNFS, Pollard's rho algorithm and brute force division.

## Execution
```bash
python shor-eng.py
```
