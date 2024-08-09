from typing import List
from app.processing.movie_processing import MovieProcessing
import networkx as nx
import matplotlib.pyplot as plt


async def build_graph(actors: List[str]) -> nx.Graph:
    movie_processing = MovieProcessing()
    graph = nx.Graph()
    
    for i, actor_url_1 in enumerate(actors):
        graph.add_node(actor_url_1)  # Добавляем узел
        
        for actor_url_2 in actors[i + 1:]:
            distance = await movie_processing.find_movie_distance(actor_url_1, actor_url_2)
            if distance != -1:
                graph.add_edge(actor_url_1, actor_url_2, weight=distance)
    
    return graph

def draw_graph(graph: nx.Graph):
    pos = nx.spring_layout(graph)
    edges = graph.edges(data=True)
    colors = []

    for u, v, data in edges:
        weight = data['weight']
        if weight == 1:
            colors.append('green')
        elif weight == 2:
            colors.append('red')
        elif weight == 3:
            colors.append('orange')
        else:
            colors.append('gray')
    
    nx.draw(graph, pos, with_labels=True, node_size=1000, node_color='lightblue', edge_color=colors, width=2, font_size=10)
    plt.show()