"""GraphAnalyzer

Clase para cargar un grafo dirigido ponderado desde JSON y ejecutar Dijkstra.
"""
from typing import Dict, List, Tuple, Any
import heapq
import json


class GraphAnalyzer:
    def __init__(self, data: Dict[str, Any], critical_threshold: float = 4.0):
        """Inicializa el analizador con datos de grafo y un umbral crítico.

        data expected format:
        {
            "nodes": [ {"id": "A", "label": "Estacion"}, ... ],
            "edges": [ ["A", "B", 2.5], ... ]
        }
        """
        self.nodes = {n['id']: n for n in data.get('nodes', [])}
        # adjacency list: node -> list of (neighbor, weight)
        self.adj: Dict[str, List[Tuple[str, float]]] = {}
        for n in self.nodes:
            self.adj[n] = []

        # Support edges defined as arrays [src, dst, weight] or objects {from, to, weight}
        for edge in data.get('edges', []):
            if isinstance(edge, dict):
                src = edge.get('from')
                dst = edge.get('to')
                w = edge.get('weight')
            else:
                # assume sequence
                try:
                    src, dst, w = edge
                except Exception:
                    continue
            if src is None or dst is None:
                continue
            # ensure nodes exist in adjacency dict
            self.adj.setdefault(src, [])
            self.adj.setdefault(dst, [])
            try:
                weight = float(w)
            except Exception:
                weight = float('inf')
            self.adj.setdefault(src, []).append((dst, weight))

        self.critical_threshold = float(critical_threshold)

    def find_shortest_path(self, start: str, end: str) -> Dict[str, Any]:
        """Aplica Dijkstra para encontrar la ruta de menor costo entre start y end.

        Returns a dict: {"path": [...], "cost": float, "critical_edges": [ (u,v,w), ... ]}

        Comentarios sobre la implementación:
        - Usamos una cola de prioridad (heap) para extraer el siguiente vértice con la
          distancia mínima conocida. Esto permite que las operaciones de extracción
          y actualización clave funcionen en O(log V) cada una en promedio, logrando
          una complejidad total aproximada de O((V + E) log V) para grafos representados
          por listas de adyacencia.
        - Estructuras usadas: diccionarios para distancias y predecesores, lista de adyacencia
          para aristas. El heap almacena tuplas (distancia, nodo).
        """
        if start not in self.adj:
            raise KeyError(f"Start node '{start}' not found in graph")
        if end not in self.adj:
            raise KeyError(f"End node '{end}' not found in graph")

        # Distancia inicial: infinito para todos menos el inicio
        dist: Dict[str, float] = {n: float('inf') for n in self.adj}
        prev: Dict[str, str] = {}

        dist[start] = 0.0
        heap: List[Tuple[float, str]] = [(0.0, start)]

        visited = set()

        while heap:
            d, u = heapq.heappop(heap)
            if u in visited:
                continue
            visited.add(u)

            if u == end:
                break

            for v, w in self.adj.get(u, []):
                alt = d + w
                # Si encontramos una ruta mejor, actualizamos
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(heap, (alt, v))

        if dist[end] == float('inf'):
            return {"path": [], "cost": float('inf'), "critical_edges": []}

        # Reconstruir camino desde end hacia start
        path = []
        node = end
        while node != start:
            path.append(node)
            node = prev.get(node)
            if node is None:
                break
        path.append(start)
        path.reverse()

        # Identificar aristas críticas en la ruta (peso < threshold)
        critical_edges = []
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            # buscar el peso
            w = next((wt for (nb, wt) in self.adj.get(u, []) if nb == v), None)
            if w is not None and w < self.critical_threshold:
                critical_edges.append((u, v, w))

        return {"path": path, "cost": dist[end], "critical_edges": critical_edges}


def load_data(filepath: str) -> Dict[str, Any]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == '__main__':
    # Quick local test when ejecutado directamente
    data = load_data('network_data.json')
    ga = GraphAnalyzer(data)
    print(ga.find_shortest_path('Workstation1', 'DB_Finanzas'))
