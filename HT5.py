#Autores: Pablo Méndez 23975
#Propósito: Simulación de corrida de programas en un sistema operativo de tiempo compartido

import simpy
import random
import matplotlib.pyplot as plt
import numpy as np

# Define la semilla para la generación de números aleatorios
RANDOM_SEED = 42

# Crea el entorno de simulación
env = simpy.Environment()

# Parámetros de la simulación
RAM = simpy.Container(env, init=100, capacity=100)
CPU = simpy.Resource(env, capacity=1)
interval = 10
random.seed(RANDOM_SEED)

# Almacena los tiempos de cada proceso
tiempos = []

def proceso(env, name, RAM, CPU):
    # Genera la cantidad de memoria y las instrucciones del proceso
    memoria = random.randint(1, 10)
    instrucciones = random.randint(1, 10)

    # Registra el tiempo de inicio
    inicio = env.now

    # El proceso llega al sistema operativo (estado "new")
    yield env.timeout(random.expovariate(1.0 / interval))

    # Solicita memoria RAM (estado "ready")
    yield RAM.get(memoria)

    while instrucciones > 0:
        # Solicita el CPU (estado "running")
        with CPU.request() as req:
            yield req
            # Ejecuta instrucciones
            for _ in range(min(instrucciones, 3)):
                yield env.timeout(1)
                instrucciones -= 1

        # Verifica si el proceso ha terminado
        if instrucciones == 0:
            # Devuelve la memoria RAM (estado "terminated")
            yield RAM.put(memoria)
            # Registra el tiempo de finalización
            tiempos.append(env.now - inicio)
            break

        # Genera un número al azar para decidir el próximo estado
        next_state = random.randint(1, 21)
        if next_state == 1:
            # El proceso pasa a la cola de "waiting"
            yield env.timeout(random.expovariate(1.0 / interval))
        # Si next_state es 2 o cualquier otro número, el proceso vuelve a "ready"

# Crea los procesos
for i in range(200):  # Cambia este número según la cantidad de procesos que quieras simular
    env.process(proceso(env, f'Proceso {i}', RAM, CPU))

# Ejecuta la simulación
env.run()

# Calcula las estadísticas
promedio = np.mean(tiempos)
desviacion = np.std(tiempos)

# Imprime las estadísticas
print(f'Tiempo promedio: {promedio}')
print(f'Desviación estándar: {desviacion}')

# Genera la gráfica
plt.figure(figsize=(10, 6))
plt.hist(tiempos, bins=20, alpha=0.5, color='g')
plt.axvline(promedio, color='r', linestyle='dashed', linewidth=2)
plt.title('Tiempo de los procesos')
plt.xlabel('Tiempo')
plt.ylabel('Número de procesos')
plt.grid(True)
plt.show()
