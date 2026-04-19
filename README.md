# Anexo: Teoría de la Información Cuántica y Computación Cuántica (FT37)

Este repositorio contiene el código fuente y las figuras generadas para el Trabajo de Fin de Grado titulado **"Teoría de la Información Cuántica y Computación Cuántica"**, presentado en la Facultad de Ciencias Físicas de la Universidad Complutense de Madrid (Curso 2025-2026).

## 📌 Correspondencia de Archivos y Resultados

La siguiente tabla vincula las secciones de la memoria con su implementación técnica y los resultados gráficos obtenidos:

| Sección | Directorio | Archivo de Código | Figura Generada | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| **Cap. 2.2**, Fig. 2 | `/Deutsch-Jozsa` | `deutsch-jozsa.py` | `deutsch-jozsa.png` | Simulación del algoritmo de Deutsch-Jozsa frente a la mejora post-cuántica y a la búsqueda aleatoria. |
| **Cap. 2.4**, Fig. 3 | `/Grover` | `grover.py` | `grover.png` | Amplificación de amplitud y búsqueda en base de datos randomizada comparando el algoritmo de Grover frente a la búsqueda lineal. |
| **Cap. 2.5**, Fig. 4 | `/Shor` | `shor.py` | `shor.png` | Factorización de enteros comparando el algoritmo de Shor con una serie de algoritmos clásicos. |

## ⚙️ Requisitos e Instalación

Las simulaciones han sido desarrolladas en **Python 3.10+**. Para ejecutarlas, se recomienda crear un entorno virtual e instalar las dependencias necesarias:

```bash
pip install numpy matplotlib qiskit qiskit-aer
```

### Instrucciones de uso:
1. Clone el repositorio: `git clone https://github.com/alvaromandado/TFG-FT37-Mandado-Diaz-Alvaro-25-26.git`
2. Acceda a la carpeta del algoritmo deseado (ej: `cd Grover`).
3. Ejecute el script: `python grover.py`.

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Siéntase libre de usar, modificar y distribuir el código, siempre que se mantenga la atribución al autor original.
