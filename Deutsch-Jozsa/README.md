# Algoritmo de Deutsch-Jozsa

Este directorio contiene la implementación del algoritmo de Deutsch-Jozsa, el primer ejemplo de un algoritmo cuántico que es exponencialmente más rápido que su análogo clásico determinista.

## Descripción
El archivo `deutsch-jozsa.py` implementa un oráculo para determinar si una función booleana oculta $f: \{0,1\}^n \rightarrow \{0,1\}$ es **constante** o **balanceada** (devuelve 0 para la mitad de las entradas y 1 para la otra mitad).

## Contenido
* **`deutsch-jozsa.py`**: Implementación utilizando Qiskit. El código construye el circuito, aplica las puertas de Hadamard, el oráculo seleccionado y mide el estado final. Además simula la búsqueda estocástica y el peor caso de la búsqueda clásica.
* **`deutsch-jozsa.png`**: Comparación de complejidad entre el algoritmo de Deutsch-Jozsa, la búsqueda clásica determinista y el método estocástico presentado por Deutsch y Jozsa.

## Ejecución
```bash
python deutsch-jozsa.py
```
