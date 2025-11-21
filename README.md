"""
================================================================================
PROYECTO: SIMULACIÓN DE TRAYECTORIAS DE ELECTRONES EN UN CAMPO MAGNÉTICO UNIFORME
================================================================================

DESCRIPCIÓN:
Este script utiliza la física clásica y la integración numérica (método de Euler)
para simular el movimiento de un electrón sometido a la Fuerza de Lorentz
en un campo magnético uniforme (B || eje X).

El script visualiza dos casos de trayectorias en 3D:
1.  Movimiento Helicoidal (Electrón disperso): Velocidad inicial perpendicular y paralela a B.
2.  Movimiento Rectilíneo Uniforme (Electrón no disperso): Velocidad inicial solo paralela a B.

El resultado es un gráfico estático 3D y una animación GIF que ilustran la
trayectoria helicoidal (azul) y la trayectoria recta (morado) a lo largo del tiempo.

REQUISITOS (INSTALACIÓN):
Para ejecutar este script, son necesarias las siguientes librerías de Python:
    pip install numpy matplotlib imageio

USO:
1.  Guarda el código como 'simulacion_electron.py'.
2.  Ejecuta desde la terminal:
        python simulacion_electron.py

SALIDA:
- Se genera un gráfico estático 3D.
- Se genera un archivo de animación: 'trayectorias_electrones.gif'

AUTOR: [Tu Nombre o Alias de GitHub]
FECHA: [Fecha de Creación o Última Modificación]
"""
