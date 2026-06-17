# Deutsch-Jozsa Algorithm

*Read this in other languages: [Español](README.md)*

This branch contains the Deutsch-Jozsa algorithm implementation. This was the first example of a quantum algorithm wich is exponentially faster than its classical deterministic analogue.

## Description
The `deutsch-jozsa-eng.py` file implements an oracle that determines whether a boolean hidden function $f: \{0,1\}^n \rightarrow \{0,1\}$ is **not constant** or **not balanced**.

## Contents
* **`deutsch-jozsa-eng.py`**: Implementation using Qiskit. The code builds the circuit, applies Hadamard gates, then the selected oracle and measures the final state. It also simulates the stochastic search and the worst classical case.
* **`deutsch-jozsa-eng.png`**: Complexity comparison between the Deutsch-Jozsa algorithm, the deterministic classical search and the stochastic algorithm.

## Execution
```bash
python deutsch-jozsa-eng.py
```
