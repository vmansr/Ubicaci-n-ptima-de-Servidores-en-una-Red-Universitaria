import pyomo.environ as pyo
import numpy as np

# Datos
facultades = [1, 2, 3, 4, 5]
nombres = ['Ingeniería', 'Ciencias', 'Economía', 'Educación', 'Salud']

costos = np.array([12000, 10000, 8000, 7000, 9500])
presupuesto = 30000

# Matriz de latencias d_{ij}
latencias = np.array([
    [2, 6, 8, 7, 9],
    [6, 2, 6, 5, 7],
    [8, 6, 2, 4, 6],
    [7, 5, 4, 2, 5],
    [9, 7, 6, 5, 2]
])

num_facultades = len(facultades)

# Modelo
model = pyo.ConcreteModel()

# Variables de decisión
model.y = pyo.Var(range(num_facultades), domain=pyo.Binary)
model.x = pyo.Var(range(num_facultades), range(num_facultades), domain=pyo.Binary)

# Función objetivo: Minimizar la latencia total
def obj_rule(model):
    return sum(latencias[i, j] * model.x[i, j] for i in range(num_facultades) for j in range(num_facultades))
model.obj = pyo.Objective(rule=obj_rule, sense=pyo.minimize)

# Restricciones

# 1. Cada facultad i debe ser atendida por exactamente un servidor j
def req_servidor_rule(model, i):
    return sum(model.x[i, j] for j in range(num_facultades)) == 1
model.req_servidor = pyo.Constraint(range(num_facultades), rule=req_servidor_rule)

# 2. Una facultad i solo puede ser atendida por j si se instaló un servidor en j
def uso_servidor_rule(model, i, j):
    return model.x[i, j] <= model.y[j]
model.uso_servidor = pyo.Constraint(range(num_facultades), range(num_facultades), rule=uso_servidor_rule)

# 3. Restricción de presupuesto
def presupuesto_rule(model):
    return sum(costos[j] * model.y[j] for j in range(num_facultades)) <= presupuesto
model.presupuesto_req = pyo.Constraint(rule=presupuesto_rule)

# Resolución
solver = pyo.SolverFactory('highs')
results = solver.solve(model, tee=False)

# Mostrar resultados
print(f"Estado de la solución: {results.solver.status}")
print(f"Condición de terminación: {results.solver.termination_condition}")

print("\n--- Resultados de la Optimización ---")
latencia_total = pyo.value(model.obj)
print(f"Latencia total mínima: {latencia_total} ms")

costo_total = sum(costos[j] * pyo.value(model.y[j]) for j in range(num_facultades))
print(f"Costo total de instalación: ${costo_total}")

print("\nUbicación de servidores:")
for j in range(num_facultades):
    if pyo.value(model.y[j]) > 0.5:
        print(f" - Facultad {facultades[j]} ({nombres[j]}) (Costo: ${costos[j]})")

print("\nAsignación de facultades a servidores:")
for i in range(num_facultades):
    for j in range(num_facultades):
        if pyo.value(model.x[i, j]) > 0.5:
            lat = latencias[i, j]
            # Usando numpy es sencillo referenciar índices 0..4
            print(f" - {nombres[i]} -> {nombres[j]} [Latencia: {lat} ms]")
