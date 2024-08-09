import asyncio
from app.config.settings import settings
from app.processing.movie_processing import MovieProcessing

from app.utils.graph_processing import build_graph, draw_graph


# Константы для актёров
ACTOR_1_URL = settings.ACTOR_1_URL
ACTOR_2_URL = settings.ACTOR_2_URL




async def main():
    movie_processing = MovieProcessing()
    distance = await movie_processing.find_movie_distance(ACTOR_1_URL, ACTOR_2_URL)
    graph = await build_graph([ACTOR_1_URL, ACTOR_2_URL])
    draw_graph(graph)
    
    print(f"Расстояние в фильмах между актёрами: {distance}")
    

asyncio.run(main())
