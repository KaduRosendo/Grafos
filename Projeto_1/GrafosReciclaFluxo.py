#!/usr/bin/env python3
# João Pedro Gianfaldoni -          10409524
# Matheus Santiago de Brito -       10408953
# Carlos Eduardo Rosendo Basseto -  10409941
# Luiz Henrique Ribeiro Pulga -     10409246
# Isabella Rodrigues de Oliveira -  10357696

import re
import sys

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
        except ValueError:
            print("Erro na leitura do tipo do grafo.")
            return None
        try:
            n = int(lines[1])
        except ValueError:
            print("Erro na leitura do número de vértices.")
            return None
        vertices = {}
        vertex_line_pattern = re.compile(r'^(\d+)\s+"([^"]*)"\s+"([^"]*)"$')
        for i in range(2, 2 + n):
            match = vertex_line_pattern.match(lines[i])
            if match:
                vid = int(match.group(1))
                label = match.group(2)
                peso = match.group(3)
                vertices[vid] = {"label": label, "peso": peso}
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
                u = int(parts[0])
                v = int(parts[1])
                peso = parts[2]
                if graph_type in [0, 1, 2, 3]:
                    key = (min(u, v), max(u, v))
                    if key not in edges:
                        edges[key] = peso
                else:
                    edges[(u, v)] = peso
            except ValueError:
                print(f"Erro ao converter dados da aresta: {lines[i]}")
                return None
        return cls(graph_type, vertices, edges)

    def write_to_file(self, filename):
        lines = []
        lines.append(str(self.graph_type))
        vertex_ids = sorted(self.vertices.keys())
        lines.append(str(len(vertex_ids)))
        for vid in vertex_ids:
            vdata = self.vertices[vid]
            lines.append(f'{vid} "{vdata["label"]}" "{vdata["peso"]}"')
        edge_lines = []
        if self.graph_type in [0, 1, 2, 3]:
            for (u, v), peso in self.edges.items():
                edge_lines.append(f"{u} {v} {peso}")
                edge_lines.append(f"{v} {u} {peso}")
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
        new_id = max(self.vertices.keys()) + 1 if self.vertices else 1
        self.vertices[new_id] = {"label": label, "peso": peso}
        print(f"Vértice inserido: id={new_id}, label='{label}', peso='{peso}'")
        return new_id

    def insert_edge(self, u, v, peso):
        if u not in self.vertices or v not in self.vertices:
            print("Um ou ambos os vértices não existem.")
            return
        if self.graph_type in [0, 1, 2, 3]:
            key = (min(u, v), max(u, v))
            if key in self.edges:
                print("Aresta já existe. Atualizando peso.")
            self.edges[key] = peso
            print(f"Aresta inserida/atualizada entre {u} e {v} com peso {peso}.")
        else:
            key = (u, v)
            if key in self.edges:
                print("Aresta já existe. Atualizando peso.")
            self.edges[key] = peso
            print(f"Aresta inserida/atualizada de {u} para {v} com peso {peso}.")

    def remove_vertex(self, vid):
        if vid not in self.vertices:
            print("Vértice não encontrado.")
            return
        del self.vertices[vid]
        removed_edges = []
        if self.graph_type in [0, 1, 2, 3]:
            for key in list(self.edges.keys()):
                if vid in key:
                    removed_edges.append(key)
                    del self.edges[key]
        else:
            for key in list(self.edges.keys()):
                if key[0] == vid or key[1] == vid:
                    removed_edges.append(key)
                    del self.edges[key]
        print(f"Vértice {vid} e suas {len(removed_edges)} arestas associadas foram removidos.")

    def remove_edge(self, u, v):
        if self.graph_type in [0, 1, 2, 3]:
            key = (min(u, v), max(u, v))
            if key in self.edges:
                del self.edges[key]
                print(f"Aresta entre {u} e {v} removida.")
            else:
                print("Aresta não encontrada.")
        else:
            key = (u, v)
            if key in self.edges:
                del self.edges[key]
                print(f"Aresta de {u} para {v} removida.")
            else:
                print("Aresta não encontrada.")

    def display_graph(self):
        print("Vértices:")
        for vid, data in sorted(self.vertices.items()):
            print(f"  {vid}: label='{data['label']}', peso='{data['peso']}'")
        print("\nArestas:")
        if self.graph_type in [0, 1, 2, 3]:
            for (u, v), peso in sorted(self.edges.items()):
                print(f"  {u} <--> {v} com peso {peso}")
        else:
            for (u, v), peso in sorted(self.edges.items()):
                print(f"  {u} --> {v} com peso {peso}")

    def get_adjacency_list(self):
        adj = {vid: [] for vid in self.vertices}
        if self.graph_type in [0, 1, 2, 3]:
            for (u, v) in self.edges.keys():
                adj[u].append(v)
                adj[v].append(u)
        else:
            for (u, v) in self.edges.keys():
                adj[u].append(v)
        return adj

    def is_connected(self):
        if not self.vertices:
            return True, []
        adj = self.get_adjacency_list()
        visited = set()
        def dfs(v):
            visited.add(v)
            for w in adj[v]:
                if w not in visited:
                    dfs(w)
        componentes = []
        for v in self.vertices:
            if v not in visited:
                comp = set()
                def dfs_comp(u):
                    comp.add(u)
                    visited.add(u)
                    for w in adj[u]:
                        if w not in comp:
                            dfs_comp(w)
                dfs_comp(v)
                componentes.append(comp)
        return (len(componentes) == 1), componentes

    def check_directed_connectivity(self):
        print("Funcionalidade para grafos direcionados não foi implementada neste exemplo.")

def show_file_content(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        print("\n--- Conteúdo do Arquivo ---")
        print(content)
        print("----------------------------\n")
    except Exception as e:
        print("Erro ao ler o arquivo:", e)

def main():
    print("==========================================")
    print("   Aplicação de Gerenciamento de Grafos   ")
    print("==========================================\n")
    graph = Graph.load_from_file(GRAFO_FILENAME)
    if graph is None:
        print("Não foi possível carregar o grafo. Encerrando.")
        sys.exit(1)
    while True:
        print("\nMenu de Opções:")
        print("a) Ler dados do arquivo grafo.txt")
        print("b) Gravar dados no arquivo grafo.txt")
        print("c) Inserir vértice")
        print("d) Inserir aresta")
        print("e) Remover vértice")
        print("f) Remover aresta")
        print("g) Mostrar conteúdo do arquivo")
        print("h) Mostrar grafo")
        print("i) Apresentar conexidade do grafo e o reduzido")
        print("j) Encerrar a aplicação")
        opc = input("Escolha uma opção: ").strip().lower()
        if opc == "a":
            novo_grafo = Graph.load_from_file(GRAFO_FILENAME)
            if novo_grafo:
                graph = novo_grafo
                print("Grafo carregado do arquivo com sucesso.")
            else:
                print("Erro ao carregar o grafo do arquivo.")
        elif opc == "b":
            graph.write_to_file(GRAFO_FILENAME)
        elif opc == "c":
            label = input("Informe o rótulo do vértice: ")
            peso = input("Informe o peso do vértice (ou deixe vazio): ")
            graph.insert_vertex(label, peso)
            graph.write_to_file(GRAFO_FILENAME)
        elif opc == "d":
            try:
                u = int(input("Informe o vértice de origem: "))
                v = int(input("Informe o vértice de destino: "))
            except ValueError:
                print("IDs de vértice devem ser numéricos.")
                continue
            peso = input("Informe o peso da aresta: ")
            graph.insert_edge(u, v, peso)
            graph.write_to_file(GRAFO_FILENAME)
        elif opc == "e":
            try:
                vid = int(input("Informe o id do vértice a remover: "))
            except ValueError:
                print("ID deve ser numérico.")
                continue
            graph.remove_vertex(vid)
            graph.write_to_file(GRAFO_FILENAME)
        elif opc == "f":
            try:
                u = int(input("Informe o vértice de origem da aresta a remover: "))
                v = int(input("Informe o vértice de destino da aresta a remover: "))
            except ValueError:
                print("IDs de vértice devem ser numéricos.")
                continue
            graph.remove_edge(u, v)
            graph.write_to_file(GRAFO_FILENAME)
        elif opc == "g":
            show_file_content(GRAFO_FILENAME)
        elif opc == "h":
            print("\n--- Exibindo Grafo ---")
            graph.display_graph()
            print("----------------------\n")
        elif opc == "i":
            if graph.graph_type in [0, 1, 2, 3]:
                conectado, componentes = graph.is_connected()
                if conectado:
                    print("O grafo é conexo.")
                else:
                    print("O grafo não é conexo.")
                    print("Componentes conexas encontradas:")
                    for idx, comp in enumerate(componentes, 1):
                        print(f"  Componente {idx}: {sorted(list(comp))}")
            else:
                graph.check_directed_connectivity()
        elif opc == "j":
            print("Encerrando a aplicação...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()