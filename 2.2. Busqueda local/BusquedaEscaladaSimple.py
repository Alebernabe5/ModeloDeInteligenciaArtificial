import random

# =========================================================================
# 1. DEFINICIÓN DEL GRAFO (DATOS DE EJEMPLO)
# =========================================================================

# Los mismos datos de ejemplo usados en Simulated Annealing.
GRAFO_SEVILLA = {
    'IES': ['A', 'B', 'C'],
    'A': ['IES', 'D'],
    'B': ['IES', 'D', 'E'],
    'C': ['IES', 'F'],
    'D': ['A', 'B', 'ESTADIO'],
    'E': ['B', 'ESTADIO'],
    'F': ['C', 'ESTADIO'],
    'ESTADIO': ['D', 'E', 'F']
}

# Costos g(n) - (Tiempo o Distancia Real)
COSTOS = {
    ('IES', 'A'): 5, ('A', 'IES'): 5,
    ('IES', 'B'): 15, ('B', 'IES'): 15,
    ('IES', 'C'): 10, ('C', 'IES'): 10,
    ('A', 'D'): 5, ('D', 'A'): 5,
    ('B', 'D'): 1, ('D', 'B'): 1, 
    ('B', 'E'): 7, ('E', 'B'): 7,
    ('C', 'F'): 8, ('F', 'C'): 8,
    ('D', 'ESTADIO'): 15, ('ESTADIO', 'D'): 15, 
    ('E', 'ESTADIO'): 4, ('ESTADIO', 'E'): 4,
    ('F', 'ESTADIO'): 5, ('ESTADIO', 'F'): 5
}

INICIO = 'IES'
META = 'ESTADIO'

# =========================================================================
# 2. FUNCIONES DE APOYO (Reutilizadas)
# =========================================================================

def calcular_costo_ruta(ruta, costos):
    """Calcula el costo total (tiempo) de una ruta dada."""
    costo_total = 0
    for i in range(len(ruta) - 1):
        origen = ruta[i]
        destino = ruta[i+1]
        costo = costos.get((origen, destino))
        
        if costo is None:
            return float('inf') 
        costo_total += costo
    return costo_total

def generar_ruta_inicial_valida(grafo, inicio, meta):
    """Genera una ruta válida aleatoria (o una ruta inicial simple)"""
    # Usaremos una ruta inicial que NO es la mejor para ver si HC la mejora
    return [inicio, 'C', 'F', meta] 

def generar_vecino(ruta, grafo, inicio, meta):
    """Genera una nueva ruta vecina válida haciendo un pequeño cambio (igual que en SA)."""
    ruta_vecina = list(ruta)
    
    if len(ruta_vecina) <= 2:
        return ruta_vecina

    # Seleccionar un índice para el nodo a cambiar (excluyendo inicio y meta)
    idx_a_cambiar = random.randint(1, len(ruta_vecina) - 2)
    nodo_anterior = ruta_vecina[idx_a_cambiar - 1]
    
    # Buscar un vecino válido del nodo_anterior para insertar
    vecinos_anteriores = grafo.get(nodo_anterior, [])
    candidatos = [n for n in vecinos_anteriores if n != inicio and n != meta and n not in ruta_vecina]
    
    if candidatos:
        # Reemplazar el nodo actual por un vecino del nodo anterior
        ruta_vecina[idx_a_cambiar] = random.choice(candidatos)
    else:
         # Si no hay candidatos, intentar cambiar la conexión a un nodo intermedio
        nodo_actual = ruta_vecina[idx_a_cambiar]
        vecinos_actuales = grafo.get(nodo_actual, [])
        candidatos_reemplazo = [n for n in vecinos_actuales if n != nodo_anterior and n != inicio and n != meta and n not in ruta_vecina]
        if candidatos_reemplazo:
            ruta_vecina[idx_a_cambiar] = random.choice(candidatos_reemplazo)


    return ruta_vecina


# =========================================================================
# 3. ALGORITMO DE ESCALADA SIMPLE (SIMPLE HILL CLIMBING)
# =========================================================================

def hill_climbing(grafo, inicio, meta, costos, max_intentos=1000):
    
    # Inicialización
    ruta_actual = generar_ruta_inicial_valida(grafo, inicio, meta)
    costo_actual = calcular_costo_ruta(ruta_actual, costos)
    
    # Bucle principal de Hill Climbing
    for i in range(max_intentos):
        
        # Generar un vecino
        ruta_vecina = generar_vecino(ruta_actual, grafo, inicio, meta)
        costo_vecino = calcular_costo_ruta(ruta_vecina, costos)

        # Asegurarse de que el vecino sea una ruta válida
        if ruta_vecina[-1] != meta or costo_vecino == float('inf'):
            continue 

        # Regla de Escalada: Aceptar solo si es mejor (menor costo)
        if costo_vecino < costo_actual:
            print(f"Mejora encontrada en intento {i+1}: Costo {costo_actual} -> {costo_vecino}")
            ruta_actual = ruta_vecina
            costo_actual = costo_vecino
            # Si se encuentra una mejora, volvemos a intentar mejorar desde el nuevo punto
            # En la versión simple, esto podría reiniciarse o continuar el bucle.
        
        elif i == max_intentos -1:
             print(f"Algoritmo detenido en intento {i+1}. No se encontraron más mejoras.")
             break
    
    return ruta_actual, costo_actual

# =========================================================================
# 4. EJECUCIÓN
# =========================================================================

print("### ESCALADA SIMPLE (HILL CLIMBING) ###")
ruta_final_hc, costo_final_hc = hill_climbing(GRAFO_SEVILLA, INICIO, META, COSTOS)

print("\n--- RESULTADO DE ESCALADA SIMPLE ---")
print(f"Ruta Inicial de Prueba: IES -> C -> F -> ESTADIO (Costo: {calcular_costo_ruta([INICIO, 'C', 'F', META], COSTOS)})")
print(f"Ruta Final HC: {' -> '.join(ruta_final_hc)}")
print(f"Costo Total HC: {costo_final_hc} unidades")
print("*" * 40) 