# Grover's Algorithm

*Read this in other languages: [Español](README.md)*

This branch contains the Grover's search algorithm implementation. This algorithm is quadratically faster than the classical linear search algorithm. It relies on the assumption that the database is unstructured.

## Description
The `grover-eng.py` script shows how **amplifyng the objective's amplitude** solves the searching problem. While a classical algorithm would need an average of $N/2$ tries to find the objective in a database with $N$ elements, Grover's algorithm only needs around $\sqrt{N}$ consults.


## Contents
* **`grover-eng.py`**: This code defines the oracle that marks the objective and the diffusion operator. It also simulates a classical linear search and the worst classical case.
* **`grover-eng.png`**: Complexity comparison between Grover's algorithm, the classical linear search and the worst classical case.

## Execution
```bash
python grover-eng.py
```
