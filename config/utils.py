# Libs:
import requests
from bs4 import BeautifulSoup
from config.config import LOGGER, EXCLUDED_KEYWORDS

# Func for config main pag:
async def fetch_page_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return BeautifulSoup(response.content.decode('utf-8', 'ignore'), 'html.parser')
    except Exception as e:
        LOGGER.error(f"Error al obtener contenido de {url}: {e}")
    return None

# Func for get info game:
async def get_game_info(url):
    soup = await fetch_page_content(url)
    if not soup:
        LOGGER.error(f"No se pudo obtener el contenido de {url}")
        return []

    titles = soup.find_all('h2', class_='gp-loop-title')
    LOGGER.debug(f"Títulos encontrados: {len(titles)}")
    games = []

    for title in titles:
        game_title = title.text.strip()
        game_link = title.find('a')['href'] if title.find('a') else None
        if game_link and not any(keyword in game_title for keyword in EXCLUDED_KEYWORDS):
            games.append((game_title, game_link))
            LOGGER.debug(f"Juego encontrado: {game_title} - {game_link}")

    return games

# Func for get weight of games:
async def get_game_weight(url):
    soup = await fetch_page_content(url)
    if not soup:
        return "No se encontró el peso del juego."
    weight_element = soup.find('strong', string='PESO TOTAL:')
    return weight_element.next_sibling.strip() if weight_element else "No se encontró el peso del juego."

# Func for get requirements:
async def get_game_requirements(url):
    soup = await fetch_page_content(url)
    if not soup:
        return "Error al obtener la página."

    title = soup.find('title').text.strip() if soup.find('title') else "Título no encontrado"
    message = f"REQUISITOS DEL SISTEMA PARA: {title}:\n"

    for req_type in ['REQUISITOS DEL SISTEMA', 'REQUISITOS MÍNIMOS']:
        req_element = soup.find('span', style='text-decoration: underline; color: #ff6600;', string=req_type)
        if req_element:
            req_list = req_element.find_next('ul')
            message += '\n'.join(f"- {req.text}" for req in req_list.find_all('li')) + "\n"

    return message