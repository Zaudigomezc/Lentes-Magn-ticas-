import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import imageio.v3 as iio
import os

# ============================================================
#   SIMULACIÓN
# ============================================================
e = 1.602e-19
m = 9.109e-31
mu0 = 4*np.pi*1e-7

R = 0.20
N = 320
I = 1.5
B0 = (8/(5*np.sqrt(5))) * mu0 * N * I / R
B = np.array([B0, 0, 0])

v1_parallel = 2e7
v1_perp_y = 2e6
v1_perp_z = 1e6

v0_1 = np.array([v1_parallel, v1_perp_y, v1_perp_z])
r0_1 = np.array([0, 0, 0])

dt = 1e-11
steps = 20000

# Trayectoria 1 (Electrón disperso - movimiento helicoidal)
r1 = np.zeros((steps,3))
v1 = np.zeros((steps,3))
r1[0] = r0_1
v1[0] = v0_1

# Integración de Euler (simple)
for i in range(steps-1):
    F = -e * np.cross(v1[i], B)
    a = F/m
    v1[i+1] = v1[i] + a*dt
    r1[i+1] = r1[i] + v1[i+1]*dt

# Trayectoria 2 (Electrón no disperso - movimiento rectilíneo uniforme)
v0_2 = np.array([v1_parallel, 0, 0])
r2 = np.zeros((steps,3))
v2 = np.zeros((steps,3))
r2[0] = r0_1
v2[0] = v0_2

for i in range(steps-1):
    # La velocidad no cambia (Fuerza de Lorentz es cero: v || B)
    v2[i+1] = v2[i]
    r2[i+1] = r2[i] + v2[i+1]*dt

# ============================================================
#  CONFIGURACIÓN VISUAL GENERAL
# ============================================================
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['font.size'] = 13

# Determinar límites del gráfico
max_r_perp = np.max([np.abs(r1[:,1]).max(), np.abs(r1[:,2]).max()]) * 1.5


# ============================================================
#  GRÁFICO ESTÁTICO CON BRILLO (MODIFICADO)
# ============================================================
fig = plt.figure(figsize=(12, 16))
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim([0, r1[-1,0] * 1.1])
ax.set_ylim([-max_r_perp, max_r_perp])
ax.set_zlim([-max_r_perp, max_r_perp])
ax.view_init(elev=20, azim=-60)

ax.set_xlabel("Eje x ($\\mathbf{B}$)")
ax.set_ylabel("Eje y")
ax.set_zlabel("Eje z")
ax.set_title("Trayectorias de Electrones colimados", fontsize=15)

# ----------------------
# BRILLO PARA r1 (MEJORADO)
# ----------------------
for w in [4, 2.5, 1.5, 1]:
    # Opacidad aumentada de 0.3 a 0.5
    ax.plot(r1[:,0], r1[:,1], r1[:,2],
            color='blue', alpha=0.3, linewidth=w)

ax.plot(r1[:,0], r1[:,1], r1[:,2],
        color='blue', linewidth=1.2,
        label='Electrón disperso en varias direcciones')

ax.scatter(r1[-1,0], r1[-1,1], r1[-1,2],
           color='red', s=80)

# ----------------------
# BRILLO PARA r2 (MEJORADO)
# ----------------------
for w in [4, 2.5, 1.5, 1]:
    # Opacidad aumentada de 0.3 a 0.5
    ax.plot(r2[:,0], r2[:,1], r2[:,2],
            color='purple', alpha=0.3, linewidth=w)

ax.plot(r2[:,0], r2[:,1], r2[:,2],
        color='purple', linestyle='--', linewidth=1.3,
        label='Electrón que no se dispersa')

ax.scatter(r2[-1,0], r2[-1,1], r2[-1,2],
           color='yellow', s=80)

# ----------------------
# Flechas del campo B
# ----------------------
NUMF = 8
x_pos = np.linspace(0, r1[-1,0], NUMF)
y_pos = np.linspace(-max_r_perp*0.6, max_r_perp*0.6, 3)
z_pos = np.linspace(-max_r_perp*0.6, max_r_perp*0.6, 3)
L = r1[-1,0] * 0.02

for x in x_pos:
    for y in y_pos:
        for z in z_pos:
            ax.quiver(x, y, z, L, 0, 0,
                      color="darkgreen",
                      alpha=0.6,
                      arrow_length_ratio=0.05)

ax.plot([], [], [], color='darkgreen', linewidth=1.5,
        label='Campo magnético paralelo al eje x')

# LEYENDA A LA IZQUIERDA
ax.legend(loc='upper left')
plt.tight_layout()
plt.show()

# ============================================================
#  ANIMACIÓN GIF 
# ============================================================
print("Generando GIF...")

NUM_FRAMES = 150              # velocidad de avance suave
STEP_FRAME = steps // NUM_FRAMES
filenames = []

for f in range(NUM_FRAMES):
    fig = plt.figure(figsize=(10, 12))
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim([0, r1[-1,0] * 1.1])
    ax.set_ylim([-max_r_perp, max_r_perp])
    ax.set_zlim([-max_r_perp, max_r_perp])
    ax.view_init(elev=20, azim=-60)

    ax.set_xlabel("Eje x ($\\mathbf{B}$)")
    ax.set_ylabel("Eje y")
    ax.set_zlabel("Eje z")
    ax.set_title("Evolución temporal de las trayectorias", fontsize=15)

    k = (f+1) * STEP_FRAME

    # ✨ Brillo animado para r1
    ax.plot(r1[:k,0], r1[:k,1], r1[:k,2],
            color='blue', linewidth=2, alpha=0.35)
    ax.plot(r1[:k,0], r1[:k,1], r1[:k,2],
            color='blue', linewidth=1.2)

    # ✨ Brillo animado para r2
    ax.plot(r2[:k,0], r2[:k,1], r2[:k,2],
            color='purple', linewidth=2, alpha=0.30)
    ax.plot(r2[:k,0], r2[:k,1], r2[:k,2],
            color='purple', linestyle="--", linewidth=1.2)

    ax.scatter(r1[k-1,0], r1[k-1,1], r1[k-1,2],
               color='red', s=60, label="Electrón disperso")
    ax.scatter(r2[k-1,0], r2[k-1,1], r2[k-1,2],
               color='yellow', s=60, label="Electrón no disperso")

    ax.plot([], [], [], color='darkgreen', linewidth=1.5,
            label='Campo magnético paralelo al eje x')
            
    # La leyenda ya estaba a la izquierda en la animación
    ax.legend(loc="upper left")

    filename = f"frame_{f:03d}.png"
    plt.savefig(filename, dpi=90)
    plt.close()
    filenames.append(filename)

# Crear GIF
images = [iio.imread(f) for f in filenames]
iio.imwrite("trayectorias_electrones.gif", images, duration=40, loop=0)

for f in filenames:
    os.remove(f)

print("GIF generado como: trayectorias_electrones.gif")
