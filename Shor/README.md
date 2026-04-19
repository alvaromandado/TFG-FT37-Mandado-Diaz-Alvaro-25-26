# Algoritmo de Shor

Este directorio contiene la simulación del algoritmo de Shor para la factorización de números enteros.

## Descripción
Debido a la complejidad computacional, el script `shor.py` calcula solo la profundidad del circuito del algoritmo de Shor, puesto que la implementación, por ejemplo, de la transformada cuántica de Fourier se hace inabarcable.

## Contenido
* **`shor.py`**: Se simulan unos cuantos casos del algoritmo rho de Pollard y la división por fuerza bruta, y se calculan las curvas teóricas de complejidad de Shor y el resto de algoritmos.
* **`shor.png`**: Comparación de complejidad entre el algoritmo de Shor, la criba del cuerpo de números, el algoritmo rho de Pollard y la división por fuerza bruta.

## Ejecución
```bash
python shor.py
```
