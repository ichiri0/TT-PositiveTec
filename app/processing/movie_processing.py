from typing import List, Optional
from collections import deque
from bs4 import BeautifulSoup
import aiohttp
import asyncio


from app.config.settings import settings


class MovieProcessing:
    
    async def fetch(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """Fetches the HTML content of a URL using aiohttp."""
        try:
            async with session.get(url) as response:
                response.raise_for_status()  # Check for HTTP errors
                return await response.text()
        except aiohttp.ClientError as e:
            print(f"HTTP error: {e} - URL: {url}")
        except Exception as e:
            print(f"Unexpected error: {e} - URL: {url}")
        return None

    async def get_movie_credits(self, actor_url: str) -> List[str]:
        """Extracts movie URLs from the actor's IMDb page."""
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, actor_url)
            if not html:
                return []

            soup = BeautifulSoup(html, 'html.parser')
            movies = []
            filmography_sections = soup.find_all('div', class_='filmo-category-section')

            for section in filmography_sections:
                section_header = section.previous_sibling.previous_sibling
                if section_header and 'actor' in section_header.get_text().lower():
                    for movie in section.find_all('div', class_='filmo-row'):
                        title_type = movie.find('b')
                        if title_type and 'TV' in title_type.get_text():
                            continue
                        link = movie.find('a')['href']
                        if link:
                            movie_url = 'https://www.imdb.com' + link + 'fullcredits'
                            if settings.DEBUG:
                                print(f"Movie URL: {movie_url}")  # Debug URL
                            movies.append(movie_url)

            return movies
    
    async def get_actors_in_movie(self, movie_url: str) -> List[str]:
        """Extracts actor URLs from the IMDb page of a movie."""
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, movie_url)
            if not html:
                return []

            soup = BeautifulSoup(html, 'html.parser')
            cast_list = soup.find('table', class_='cast_list')
            if not cast_list:
                return []

            actors = []
            for row in cast_list.find_all('tr'):
                actor = row.find('td', class_='primary_photo')
                if actor:
                    actor_link = actor.find('a')['href']
                    full_actor_link = 'https://www.imdb.com' + actor_link + 'fullcredits'
                    print(f"Actor URL: {full_actor_link}")  # Debug URL
                    actors.append(full_actor_link)

            return actors

    async def get_actors_in_movie_parallel(self, movie_urls: List[str]) -> List[str]:
        """Fetches actors from multiple movies in parallel."""
        async with aiohttp.ClientSession() as session:
            tasks = [self.get_actors_in_movie(movie_url) for movie_url in movie_urls]
            results = await asyncio.gather(*tasks)

        actors = [actor for result in results for actor in result]
        return actors

    async def find_movie_distance(self, actor_1_url: str, actor_2_url: str) -> int:
        """Finds the shortest distance between two actors based on shared movies."""
        queue = deque([(actor_1_url, 0)])
        visited = set()

        while queue:
            current_actor_url, distance = queue.popleft()
            if current_actor_url in visited:
                continue
            visited.add(current_actor_url)
            movies = await self.get_movie_credits(current_actor_url)
            for movie_url in movies:
                actors_in_movie = await self.get_actors_in_movie_parallel([movie_url])
                if actor_2_url in actors_in_movie:
                    return distance + 1
                for actor in actors_in_movie:
                    if actor not in visited:
                        queue.append((actor, distance + 1))
        
        return -1
