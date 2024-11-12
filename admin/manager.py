# Libs:
import json
from config.config import DATA_FILE, LOGGER

# Func for Load Data from Json File:
def load_data(bot):
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            channel_id = data.get('channel_id')
            if channel_id:
                bot.channel_id = int(channel_id)
            else:
                bot.channel_id = None
            bot.prev_titles = set(data.get('prev_titles', []))
            bot.tracked_games = data.get('tracked_games', {})
            LOGGER.info("Datos cargados exitosamente.")
    except FileNotFoundError:
        bot.channel_id = None
        bot.prev_titles = set()
        bot.tracked_games = {}
        LOGGER.info("No se encontró archivo de datos previo.")
    except Exception as e:
        LOGGER.error(f"Error al cargar datos: {e}")
        bot.channel_id = None
        bot.prev_titles = set()
        bot.tracked_games = {}

# Func for Save Data Into Json File:
def save_data(bot):
    try:
        data = {
            'channel_id': bot.channel_id if bot.channel_id else None,
            'prev_titles': list(bot.prev_titles),
            'tracked_games': bot.tracked_games
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        LOGGER.info("Datos guardados exitosamente.")
    except Exception as e:
        LOGGER.error(f"Error al guardar datos: {e}")

