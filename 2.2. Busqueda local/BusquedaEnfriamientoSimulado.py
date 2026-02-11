import random
import math


# 1. DEFINICIÓN DEL GRAFO (DATOS DE EJEMPLO)



# Nodos: IES (Inicio) y ESTADIO (Meta).
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
    ('B', 'D'): 1, ('D', 'B'): 1, # El camino corto "secreto"
    ('B', 'E'): 7, ('E', 'B'): 7,
    ('C', 'F'): 8, ('F', 'C'): 8,
    ('D', 'ESTADIO'): 15, ('ESTADIO', 'D'): 15, # El camino caro
    ('E', 'ESTADIO'): 4, ('ESTADIO', 'E'): 4,
    ('F', 'ESTADIO'): 5, ('ESTADIO', 'F'): 5
}

INICIO = 'IES'
META = 'ESTADIO'

# =========================================================================
# 2. FUNCIONES DE APOYO
# =========================================================================

def calcular_costo_ruta(ruta, costos):
    """Calcula el costo total (tiempo) de una ruta dada."""
    costo_total = 0
    for i in range(len(ruta) - 1):
        origen = ruta[i]
        destino = ruta[i+1]
        costo = costos.get((origen, destino))
        
        # Si un segmento no es válido o no tiene costo, la ruta es inválida
        if costo is None:
            return float('inf') 
        costo_total += costo
    return costo_total

def generar_ruta_inicial_valida(grafo, inicio, meta):
    """Genera una ruta válida aleatoria (o una ruta inicial simple)"""
    # Para este ejemplo, usaremos una ruta simple que pasa por el nodo B
    try:
        if 'B' in grafo[inicio]:
            return [inicio, 'B', 'E', meta] # Ruta simple de ejemplo
    except KeyError:
        # Fallback si el inicio no tiene B, etc.
        return [inicio, 'A', 'D', meta]

# El operador de vecindad es clave en SA. Aquí, cambiamos un nodo intermedio.
def generar_vecino(ruta, grafo, inicio, meta):
    """Genera una nueva ruta vecina válida haciendo un pequeño cambio."""
    ruta_vecina = list(ruta)
    
    # Solo cambiamos los nodos intermedios (no inicio ni meta)
    if len(ruta_vecina) <= 2:
        return ruta_vecina

    # 1. Seleccionar un índice para el nodo a cambiar (excluyendo inicio y meta)
    idx_a_cambiar = random.randint(1, len(ruta_vecina) - 2)
    nodo_anterior = ruta_vecina[idx_a_cambiar - 1]
    nodo_siguiente = ruta_vecina[idx_a_cambiar + 1]

    # 2. Buscar posibles reemplazos (vecinos comunes de anterior y siguiente, o re-enrutar)
    vecinos_anteriores = grafo.get(nodo_anterior, [])
    candidatos = [n for n in vecinos_anteriores if n != nodo_siguiente and n != nodo_anterior and n not in ruta_vecina]
    
    # 3. Si hay candidatos, reemplazamos
    if candidatos:
        ruta_vecina[idx_a_cambiar] = random.choice(candidatos)
    # 4. Si no, insertamos un nodo vecino válido al azar
    else:
        vecinos_del_nodo_anterior = grafo.get(nodo_anterior, [])
        nuevo_nodo = random.choice([n for n in vecinos_del_nodo_anterior if n != inicio])
        ruta_vecina.insert(idx_a_cambiar, nuevo_nodo)
        
    return ruta_vecina

# =========================================================================
# 3. ALGORITMO DE ENFRIAMIENTO SIMULADO
# =========================================================================

def simulated_annealing(grafo, inicio, meta, costos, T_inicial=100.0, factor_enfriamiento=0.99, iteraciones_max=1000):
    
    # Inicialización
    ruta_actual = generar_ruta_inicial_valida(grafo, inicio, meta)
    costo_actual = calcular_costo_ruta(ruta_actual, costos)
    
    mejor_ruta = ruta_actual
    mejor_costo = costo_actual
    
    temperatura = T_inicial

    print(f"Ruta inicial: {' -> '.join(ruta_actual)} | Costo: {costo_actual}")
    print("-" * 40)

    for i in range(iteraciones_max):
        # 1. Generar un vecino
        ruta_vecina = generar_vecino(ruta_actual, grafo, inicio, meta)
        costo_vecino = calcular_costo_ruta(ruta_vecina, costos)
        
        # Verificar si la ruta sigue siendo válida (llega al destino)
        if ruta_vecina[-1] != meta:
            # Si el vecino no es válido, se sigue intentando en la misma iteración
            continue 

        # 2. Calcular diferencia de energía/costo
        delta_costo = costo_vecino - costo_actual

        # 3. Decisión de Transición
        
        # A) Aceptar si es mejor (delta_costo es negativo)
        if delta_costo < 0:
            ruta_actual = ruta_vecina
            costo_actual = costo_vecino
            
            # Actualizar el mejor global
            if costo_actual < mejor_costo:
                mejor_costo = costo_actual
                mejor_ruta = ruta_actual
        
        # B) Aceptar si es peor con una probabilidad (probabilidad de escape)
        else:
            if temperatura > 0:
                # Fórmula de Metropolis: e^(-delta_costo / T)
                probabilidad = math.exp(-delta_costo / temperatura)
                if random.random() < probabilidad:
                    ruta_actual = ruta_vecina
                    costo_actual = costo_vecino
        
        # 4. Enfriamiento (Schedule)
        temperatura *= factor_enfriamiento
        
        if i % 100 == 0:
            print(f"Iteración {i:04d} | Temp: {temperatura:.2f} | Costo Actual: {costo_actual:.1f} | Mejor Costo: {mejor_costo:.1f}")
        
        # Detener si la temperatura es demasiado baja
        if temperatura < 0.1:
            break

    return mejor_ruta, mejor_costo

# =========================================================================
# 4. EJECUCIÓN
# =========================================================================

print("### INICIO DE ENFRIAMIENTO SIMULADO (SIMULATED ANNEALING) ###")

# Parámetros del algoritmo
T_INICIAL = 1000.0   # Temperatura inicial alta
FACTOR_ENFRIAMIENTO = 0.999 # Factor de reducción de temperatura
MAX_ITERACIONES = 5000

ruta_final_sa, costo_final_sa = simulated_annealing(
    GRAFO_SEVILLA, INICIO, META, COSTOS,
    T_inicial=T_INICIAL, factor_enfriamiento=FACTOR_ENFRIAMIENTO, iteraciones_max=MAX_ITERACIONES
)

print("\n--- RESULTADO FINAL DE LA BÚSQUEDA LOCAL ---")
print(f"**Ruta Recomendada para el Tutor (Enfriamiento Simulado):**")
print(f"Ruta: {' -> '.join(ruta_final_sa)}")
print(f"Costo Total Estimado (Tiempo): {costo_final_sa} unidades")
print("*" * 40)