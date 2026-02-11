#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque
import heapq
from grafo import ruta_euclidea as graph   

# ---------------------------------------------------------
# Paso 1: Búsqueda en anchura (BFS)

def bfs(graph, start, goal):
    queue = deque([[start]])
    visited = set([start])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            return path

        for neighbor in graph.get(node, {}):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    return None


# ---------------------------------------------------------
# Paso 2: Búsqueda en profundidad (DFS)

def dfs(graph, start, goal):
    stack = [[start]]
    visited = set([start])

    while stack:
        path = stack.pop()
        node = path[-1]

        if node == goal:
            return path

        for neighbor in graph.get(node, {}):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                stack.append(new_path)
    return None


# ---------------------------------------------------------
# Paso 3: Búsqueda de coste uniforme (UCS)

def ucs(graph, start, goal):
    """
    Búsqueda de coste uniforme (Uniform Cost Search)
    Devuelve el camino más barato y su coste total.
    """
    priority_queue = [(0, [start])]  # (coste_acumulado, camino)
    visited = set()

    while priority_queue:
        cost, path = heapq.heappop(priority_queue)
        node = path[-1]

        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            return path, cost

        for neighbor, weight in graph.get(node, {}).items():
            if neighbor not in visited:
                new_cost = cost + weight
                new_path = path + [neighbor]
                heapq.heappush(priority_queue, (new_cost, new_path))

    return None, float('inf')


# ---------------------------------------------------------
# Paso 4: Búsqueda Voraz (Greedy Best-First Search)

def greedy_best_first(graph, start, goal):
    """
    Búsqueda voraz (Greedy Best-First Search)
    Expande siempre el nodo más cercano al objetivo según la heurística h(n).
    """
    from queue import PriorityQueue

    def heuristic(node):
        """
        Heurística: distancia directa si existe conexión,
        o la mínima de sus vecinos como estimación.
        """
        if goal in graph.get(node, {}):
            return graph[node][goal]
        else:
            return min(graph[node].values()) if graph.get(node) else float('inf')

    pq = PriorityQueue()
    pq.put((0, [start]))
    visited = set()

    while not pq.empty():
        _, path = pq.get()
        node = path[-1]

        if node == goal:
            return path

        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, {}):
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    priority = heuristic(neighbor)
                    pq.put((priority, new_path))

    return None


# ---------------------------------------------------------
# Paso 5: Algoritmo A* (A estrella)

def a_star(graph, start, goal):
    """
    Algoritmo A* (A estrella)
    Combina el coste real (g) con una heurística estimada (h).
    """
    from queue import PriorityQueue

    def heuristic(node):
        """
        Heurística simple: distancia directa si existe conexión,
        o la mínima de sus vecinos como estimación.
        """
        if goal in graph.get(node, {}):
            return graph[node][goal]
        else:
            return min(graph[node].values()) if graph.get(node) else float('inf')

    pq = PriorityQueue()
    pq.put((0, 0, [start]))  # (f = g + h, g, camino)
    visited = set()

    while not pq.empty():
        f, g, path = pq.get()
        node = path[-1]

        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            return path, g  # camino y coste real acumulado

        for neighbor, cost in graph.get(node, {}).items():
            if neighbor not in visited:
                g_new = g + cost
                f_new = g_new + heuristic(neighbor)
                pq.put((f_new, g_new, path + [neighbor]))

    return None, float('inf')


# ---------------------------------------------------------
# Ejecución principal

if __name__ == "__main__":
    start = "IES Punta del Verde"
    goal = "Estadio La Cartuja\t"  # ⚠️ cuidado con el tabulador en el nombre

    # BFS
    print("\n--- BÚSQUEDA EN ANCHURA (BFS) ---")
    path_bfs = bfs(graph, start, goal)
    if path_bfs:
        print("Camino BFS:", " → ".join(path_bfs))
        print(f"Pasos: {len(path_bfs) - 1}")
    else:
        print("No se encontró un camino con BFS.")

    # DFS
    print("\n--- BÚSQUEDA EN PROFUNDIDAD (DFS) ---")
    path_dfs = dfs(graph, start, goal)
    if path_dfs:
        print("Camino DFS:", " → ".join(path_dfs))
        print(f"Pasos: {len(path_dfs) - 1}")
    else:
        print("No se encontró un camino con DFS.")

    # UCS
    print("\n--- BÚSQUEDA DE COSTE UNIFORME (UCS) ---")
    path_ucs, cost_ucs = ucs(graph, start, goal)
    if path_ucs:
        print("Camino UCS:", " → ".join(path_ucs))
        print(f"Coste total: {cost_ucs} unidades")
    else:
        print("No se encontró un camino con UCS.")

    # GREEDY BEST-FIRST SEARCH
    print("\n--- BÚSQUEDA VORAZ (GREEDY BEST-FIRST) ---")
    path_greedy = greedy_best_first(graph, start, goal)
    if path_greedy:
        print("Camino Greedy:", " → ".join(path_greedy))
        print(f"Pasos: {len(path_greedy) - 1}")
    else:
        print("No se encontró un camino con la búsqueda voraz.")

    # A*
    print("\n--- ALGORITMO A* (A ESTRELLA) ---")
    path_astar, cost_astar = a_star(graph, start, goal)
    if path_astar:
        print("Camino A*:", " → ".join(path_astar))
        print(f"Coste total: {cost_astar} unidades")
    else:
        print("No se encontró un camino con A*.")
