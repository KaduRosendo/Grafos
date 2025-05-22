
#!/usr/bin/env python3
# João Pedro Gianfaldoni -          10409524
# Matheus Santiago de Brito -       10408953
# Carlos Eduardo Rosendo Basseto -  10409941
# Luiz Henrique Ribeiro Pulga -     10409246

import re
import sys
import heapq

GRAFO_FILENAME = "grafo.txt"

class Graph:
    def __init__(self, graph_type, vertices, edges):
        self.graph_type = graph_type
        self.vertices = vertices
        self.edges = edges

    @classmethod
    def load_from_file(cls, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Arquivo {filename} não encontrado.")
            return None
        try:
            graph_type = int(lines[0])
            n = int(lines[1])
        except ValueError:
            print("Erro na leitura do tipo ou número de vértices.")
            return None
        vertices = {}
        vertex_line_pattern = re.compile(r'^(\d+)\s+"([^"]*)"\s+"([^"]*)"$')
        for i in range(2, 2 + n):
            match = vertex_line_pattern.match(lines[i])
            if match:
                vid = int(match.group(1))
                vertices[vid] = {"label": match.group(2), "peso": match.group(3)}
            else:
                print(f"Erro ao ler a linha de vértice: {lines[i]}")
                return None
        try:
            m = int(lines[2 + n])
        except ValueError:
            print("Erro na leitura do número de arestas.")
            return None
        edges = {}
        for i in range(3 + n, 3 + n + m):
            parts = lines[i].split()
            if len(parts) < 3:
                print(f"Erro ao ler a linha de aresta: {lines[i]}")
                return None
            try:
                u, v = int(parts[0]), int(parts[1])
                peso = parts[2]
                key = (min(u, v), max(u, v)) if graph_type in [0, 1, 2, 3] else (u, v)
                edges[key] = peso
            except ValueError:
                print(f"Erro ao converter dados da aresta: {lines[i]}")
                return None
        return cls(graph_type, vertices, edges)

    def write_to_file(self, filename):
        lines = [str(self.graph_type), str(len(self.vertices))]
        for vid in sorted(self.vertices):
            v = self.vertices[vid]
            lines.append(f'{vid} "{v["label"]}" "{v["peso"]}"')
        edge_lines = []
        if self.graph_type in [0, 1, 2, 3]:
            for (u, v), peso in self.edges.items():
                edge_lines.extend([f"{u} {v} {peso}", f"{v} {u} {peso}"])
        else:
            for (u, v), peso in self.edges.items():
                edge_lines.append(f"{u} {v} {peso}")
        lines.append(str(len(edge_lines)))
        lines.extend(edge_lines)
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("\n".join(lines))
            print("Arquivo atualizado com sucesso!")
        except Exception as e:
            print("Erro ao escrever no arquivo:", e)

    def insert_vertex(self, label, peso):
        new_id = max(self.vertices.keys(), default=0) + 1
        self.vertices[new_id] = {"label": label, "peso": peso}
        print(f"Vértice inserido: id={new_id}, label='{label}', peso='{peso}'")
        return new_id

    def insert_edge(self, u, v, peso):
        if u not in self.vertices or v not in self.vertices:
            print("Um ou ambos os vértices não existem.")
            return
        key = (min(u, v), max(u, v)) if self.graph_type in [0, 1, 2, 3] else (u, v)
        self.edges[key] = peso
        print(f"Aresta inserida/atualizada entre {u} e {v} com peso {peso}.")

    def remove_vertex(self, vid):
        if vid not in self.vertices:
            print("Vértice não encontrado.")
            return
        del self.vertices[vid]
        self.edges = {k: v for k, v in self.edges.items() if vid not in k}
        print(f"Vértice {vid} e suas arestas foram removidos.")

    def remove_edge(self, u, v):
        key = (min(u, v), max(u, v)) if self.graph_type in [0, 1, 2, 3] else (u, v)
        if key in self.edges:
            del self.edges[key]
            print(f"Aresta entre {u} e {v} removida.")
        else:
            print("Aresta não encontrada.")

    def display_graph(self):
        print("Vértices:")
        for vid, data in sorted(self.vertices.items()):
            print(f"  {vid}: label='{data['label']}', peso='{data['peso']}'")
        print("\nArestas:")
        for (u, v), peso in sorted(self.edges.items()):
            if self.graph_type in [0, 1, 2, 3]:
                print(f"  {u} <--> {v} com peso {peso}")
            else:
                print(f"  {u} --> {v} com peso {peso}")

    def get_adjacency_list(self):
        adj = {v: [] for v in self.vertices}
        for (u, v) in self.edges:
            adj[u].append(v)
            if self.graph_type in [0, 1, 2, 3]:
                adj[v].append(u)
        return adj

    def is_connected(self):
        if not self.vertices:
            return True, []
        visited = set()
        def dfs(v):
            visited.add(v)
            for w in self.get_adjacency_list()[v]:
                if w not in visited:
                    dfs(w)
        componentes = []
        for v in self.vertices:
            if v not in visited:
                comp = set()
                def dfs_comp(x):
                    comp.add(x)
                    visited.add(x)
                    for w in self.get_adjacency_list()[x]:
                        if w not in comp:
                            dfs_comp(w)
                dfs_comp(v)
                componentes.append(comp)
        return (len(componentes) == 1), componentes

    def check_directed_connectivity(self):
        print("Funcionalidade para grafos direcionados não foi implementada neste exemplo.")

def dijkstra(graph, start):
    distances = {v: float('inf') for v in graph.vertices}
    distances[start] = 0
    heap = [(0, start)]
    while heap:
        dist, u = heapq.heappop(heap)
        for v in graph.get_adjacency_list()[u]:
            key = (min(u, v), max(u, v)) if graph.graph_type in [0,1,2,3] else (u, v)
            weight = float(graph.edges.get(key, float('inf')))
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                heapq.heappush(heap, (distances[v], v))
    return distances

def encontrar_ponto_mais_proximo(graph):
    try:
        origem = int(input("Informe o ID do vértice onde você está: "))
    except ValueError:
        print("ID inválido.")
        return
    if origem not in graph.vertices:
        print("Vértice não encontrado.")
        return
    distancias = dijkstra(graph, origem)
    mais_proximo = sorted((v, d) for v, d in distancias.items() if v != origem and d < float('inf'))
    if not mais_proximo:
        print("Nenhum ponto acessível.")
    else:
        for v, d in mais_proximo:
            print(f"  {v} - {graph.vertices[v]['label']} a {d} de distância")

def prim_mst(graph):
    if not graph.vertices:
        print("Grafo vazio.")
        return
    start = next(iter(graph.vertices))
    visited = {start}
    edges = []
    total = 0
    while len(visited) < len(graph.vertices):
        candidates = [
            (float(graph.edges[(min(u, v), max(u, v))]), u, v)
            for u in visited for v in graph.get_adjacency_list()[u]
            if v not in visited and (min(u, v), max(u, v)) in graph.edges
        ]
        if not candidates:
            print("Grafo não é conexo.")
            return
        cost, u, v = min(candidates)
        visited.add(v)
        edges.append((u, v, cost))
        total += cost
    print("Árvore Geradora Mínima:")
    for u, v, c in edges:
        print(f"  {u} <--> {v} com custo {c}")
    print(f"Custo total: {total}")

def colorir_vertices(graph):
    cores = {}
    adj = graph.get_adjacency_list()

    for vertice in sorted(graph.vertices):
        usadas = {cores[vizinho] for vizinho in adj[vertice] if vizinho in cores}
        cor = 1
        while cor in usadas:
            cor += 1
        cores[vertice] = cor

    print("\nColoração de Vértices (número mínimo de cores):")
    for v in sorted(cores):
        print(f"  Vértice {v} ({graph.vertices[v]['label']}) -> Cor {cores[v]}")
    print(f"Total de cores usadas: {max(cores.values())}")

def main():
    print("=== Gerenciamento de Grafos ===")
    graph = Graph.load_from_file(GRAFO_FILENAME)
    if not graph:
        return
    while True:
        print("\nMenu:")
        print("a) Ler grafo")
        print("b) Gravar grafo")
        print("c) Inserir vértice")
        print("d) Inserir aresta")
        print("e) Remover vértice")
        print("f) Remover aresta")
        print("g) Mostrar arquivo")
        print("h) Mostrar grafo")
        print("i) Verificar conexidade")
        print("j) Sair")
        print("k) Caminho mínimo (Dijkstra)")
        print("l) Árvore Geradora Mínima (Prim)")
        print("m) Coloração de Vértices")
        opc = input("Opção: ").lower().strip()
        if opc == "a":
            graph = Graph.load_from_file(GRAFO_FILENAME)
        elif opc == "b":
            graph.write_to_file(GRAFO_FILENAME)
        elif opc == "c":
            label = input("Rótulo: ")
            peso = input("Peso: ")
            graph.insert_vertex(label, peso)
        elif opc == "d":
            u = int(input("Origem: "))
            v = int(input("Destino: "))
            peso = input("Peso: ")
            graph.insert_edge(u, v, peso)
        elif opc == "e":
            vid = int(input("Vértice a remover: "))
            graph.remove_vertex(vid)
        elif opc == "f":
            u = int(input("Origem: "))
            v = int(input("Destino: "))
            graph.remove_edge(u, v)
        elif opc == "g":
            with open(GRAFO_FILENAME, encoding='utf-8') as f:
                print(f.read())
        elif opc == "h":
            graph.display_graph()
        elif opc == "i":
            conexo, componentes = graph.is_connected()
            print("Conexo." if conexo else f"Não conexo. Componentes: {componentes}")
        elif opc == "j":
            break
        elif opc == "k":
            encontrar_ponto_mais_proximo(graph)
        elif opc == "l":
            prim_mst(graph)
        elif opc == "m":
            colorir_vertices(graph)
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
