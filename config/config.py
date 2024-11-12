# Libs:
import logging

# Config Loggs:
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

# URL:
PIVIGAMES_URL = 'https://pivigames.blog/'

# Config Excluded Ads:
EXCLUDED_KEYWORDS = [
    'Oferta -25%', 'Oferta -50%', 'Oferta -95%', 'Oferta -32%',
    'SORTEO', 'ESTÁN REGALANDO', 'CRUNCHYROLL', 'TOP', 'Oferta',
    'LOS MEJORES JUEGOS'
]

# Config DB:
DATA_FILE = 'config.json'


