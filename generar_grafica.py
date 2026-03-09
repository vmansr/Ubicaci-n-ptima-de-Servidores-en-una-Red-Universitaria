import matplotlib.pyplot as plt
import networkx as nx

# Nodos y posiciones aproximadas para darle buena apariencia (mapa ficticio de facultades)
nombres = {
    1: 'Ingeniería',
    2: 'Ciencias',
    3: 'Economía',
    4: 'Educación',
    5: 'Salud'
}

# (x, y) Layout manual para que quede estético
pos = {
    1: (0, 2),
    2: (1, 3),
    3: (2, 2.5),
    4: (2, 1),
    5: (3.5, 1.5)
}

G = nx.DiGraph()

# Añadir nodos
for i, nombre in nombres.items():
    G.add_node(i, label=nombre)

# Enlaces de asignación (decisión tomada por el modelo óptimo)
# 1->1, 2->2, 3->4, 4->4, 5->4
asignaciones = [
    (1, 1, 2),  # Ingeniería -> Ingeniería (Latencia 2)
    (2, 2, 2),  # Ciencias -> Ciencias (Latencia 2)
    (3, 4, 4),  # Economía -> Educación (Latencia 4)
    (4, 4, 2),  # Educación -> Educación (Latencia 2)
    (5, 4, 5)   # Salud -> Educación (Latencia 5)
]

for origen, destino, latencia in asignaciones:
    if origen != destino:
        G.add_edge(origen, destino, weight=latencia)

# Crear la figura
plt.figure(figsize=(9, 6), facecolor='white')

# Dibujar nodos
node_colors = ['#87CEFA' if i in [1, 2, 4] else '#D3D3D3' for i in range(1, 6)]
# Los nodos con servidor (1, 2, 4) se pintan de un color diferente (azul claro), los otros gris
nx.draw_networkx_nodes(G, pos, node_size=3500, node_color=node_colors, edgecolors='black', linewidths=1.5)

# Dibujar etiquetas de nodos
node_labels = {i: nombres[i] for i in range(1, 6)}
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=11, font_family="sans-serif", font_weight='bold')

# Dibujar aristas
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2, alpha=0.7, arrowsize=20, edge_color='black', connectionstyle='arc3,rad=0.1')

# Dibujar etiquetas de aristas (latencias)
edge_labels = {(u, v): f"{d['weight']} ms" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_weight='bold', font_color='red')

# Añadir un indicador de servidor local para los q se atienden a sí mismos
for n in [1, 2, 4]:
    x, y = pos[n]
    plt.text(x, y - 0.25, "[Servidor Local: 2 ms]", fontsize=9, ha='center', color='blue', fontweight='bold')

plt.title("Figura 1. Grafo de asignación óptima de servidores y latencias", fontsize=14, fontweight='bold', pad=20)
plt.axis('off')
plt.tight_layout()

# Guardar
plt.savefig('grafo_asignacion_apa.png', dpi=300, bbox_inches='tight')
plt.close()
