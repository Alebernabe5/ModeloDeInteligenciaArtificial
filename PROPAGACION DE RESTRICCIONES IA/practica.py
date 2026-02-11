import matplotlib.pyplot as plt
import networkx as nx 

# --- FUNCIONES DE RESTRICCIÓN Y VISUALIZACIÓN ---

def constraint(var1, val1, var2, val2):
    """
    Función de restricción: No hay dos regiones adyacentes que puedan tener el mismo color.
    """
    return val1 != val2

def visualize_solution(solution, neighbors):
    """
    Visualiza la solución usando matplotlib y networkx.
    """
    G = nx.Graph()
    for var in solution:
        G.add_node(var, color=solution[var])
    for var, neighs in neighbors.items():
        for neigh in neighs:
            # Asegura que la arista se añade solo una vez
            if var < neigh: 
                G.add_edge(var, neigh)
    
    # Mapeo de colores para networkx/matplotlib
    color_map = {'Rojo': '#FF5733', 'Verde': '#33FF57', 'Azul': '#3357FF', 'Amarillo': '#FFC300'}
    colors = [color_map.get(G.nodes[node]['color'], '#808080') for node in G.nodes]
    
    pos = nx.spring_layout(G, seed=10) # Usar un seed para layout reproducible
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, 
            with_labels=True, 
            node_color=colors, 
            node_size=4000, 
            font_size=12, 
            font_color='black', 
            font_weight='bold',
            edge_color='gray')
    plt.title("Coloreado de Provincias de Andalucía (CSP)")
    plt.show()

# --- CLASE CSP (CON MÉTODOS ANIDADOS) ---
# (La lógica interna de la clase CSP se mantiene sin cambios)

class CSP:
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints

    def is_consistent(self, var, assignment):
        for neighbor in self.neighbors[var]:
            if neighbor in assignment:
                if not self.constraints(var, assignment[var], neighbor, assignment[neighbor]):
                    return False
        return True

    def ac3(self):
        queue = [(xi, xj) for xi in self.variables for xj in self.neighbors[xi]]
        while queue:
            (xi, xj) = queue.pop(0)
            if self.revise(xi, xj):
                if len(self.domains[xi]) == 0: return False
                for xk in self.neighbors[xi]:
                    if xk != xj: queue.append((xk, xi))
        return True

    def revise(self, xi, xj):
        revised = False
        for x in list(self.domains[xi]):
            if not any(self.constraints(xi, x, xj, y) for y in self.domains[xj]):
                self.domains[xi].remove(x)
                revised = True
        return revised
    
    def backtracking_search(self, assignment={}):
        if len(assignment) == len(self.variables): return assignment
        
        var = self.select_unassigned_variable(assignment)
        
        for value in self.domains[var]:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            
            if self.is_consistent(var, new_assignment):
                result = self.backtracking_search(new_assignment)
                if result: return result
        
        return None

    def select_unassigned_variable(self, assignment):
        for var in self.variables:
            if var not in assignment: return var
        return None

# --- DEFINICIÓN DEL PROBLEMA DE PROVINCIAS DE ANDALUCÍA ---

variables = ['AL', 'CA', 'CO', 'GR', 'HU', 'JA', 'MA', 'SE']
nombre_provincia = {
    'AL': 'Almería', 'CA': 'Cádiz', 'CO': 'Córdoba', 'GR': 'Granada', 
    'HU': 'Huelva', 'JA': 'Jaén', 'MA': 'Málaga', 'SE': 'Sevilla'
}

# Dominio de 3 colores
domains = {
    var: ['Rojo', 'Verde', 'Azul'] for var in variables
}

# Adyacencias (Fronteras terrestres entre provincias)
neighbors = {
    # Almería (AL) limita con:
    'AL': ['GR'],
    # Cádiz (CA) limita con:
    'CA': ['SE', 'MA'],
    # Córdoba (CO) limita con:
    'CO': ['SE', 'JA', 'GR', 'MA'],
    # Granada (GR) limita con:
    'GR': ['AL', 'JA', 'CO', 'MA'],
    # Huelva (HU) limita con:
    'HU': ['SE'],
    # Jaén (JA) limita con:
    'JA': ['CO', 'GR'],
    # Málaga (MA) limita con:
    'MA': ['CA', 'SE', 'CO', 'GR'],
    # Sevilla (SE) limita con:
    'SE': ['HU', 'CA', 'MA', 'CO']
}

# --- EJECUCIÓN ---

csp = CSP(variables, domains, neighbors, constraint)

print("Iniciando AC-3 para propagación de restricciones...")

if csp.ac3():
    print("AC-3 finalizado. Buscando solución con Backtracking...")
    solution = csp.backtracking_search()
    
    if solution:
        print("\n✅ Solución encontrada (Coloreado de Provincias de Andalucía):")
        for var in variables:
            print(f"  {var} ({nombre_provincia[var]}): Color {solution[var]}")
        
        visualize_solution(solution, neighbors)
    else:
        print("\n❌ No se encontró solución.")
else:
    print("\n❌ No se encontró solución (AC-3 vació el dominio de una variable).")