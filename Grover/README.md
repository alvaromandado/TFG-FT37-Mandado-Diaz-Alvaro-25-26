# Algoritmo de Grover

Este directorio contiene la implementación del algoritmo de búsqueda de Grover, que proporciona una aceleración cuadrática para problemas de búsqueda en bases de datos no estructuradas (sin información adicional sobre la ubicación de los elementos en la propia base).

## Descripción
El script `grover.py` demuestra la **amplificación de amplitud**. Mientras que un algoritmo clásico necesitaría $N/2$ consultas de media para encontrar un elemento marcado en una lista de tamaño $N$, Grover lo logra en aproximadamente $\sqrt{N}$ consultas.

## Contenido
* **`grover.py`**: Código que define el oráculo que marca el estado objetivo y el operador de difusión que refleja las amplitudes sobre la media. Además simula la búsqueda lineal clásica y el peor caso de la misma.
* **`grover.png`**: Comparación de complejidad entre el algoritmo de Grover, la búsqueda lineal clásica y el peor caso de la misma.

## Ejecución
```bash
python grover.py
```
