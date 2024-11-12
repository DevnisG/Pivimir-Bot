# Libs:
import os
import asyncio
from discord import Intents
from discord.ext import commands
from config.config import LOGGER
from admin.manager import load_data

# BOT Config:
intents = Intents.default()
intents.message_content = True
intents.guilds = True
intents.reactions = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

# Func MAIN:
async def main():
    load_data(bot)

    await bot.load_extension('commands.admin_commands')
    await bot.load_extension('commands.game_commands')
    await bot.load_extension('tasks.game_tasks')

    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    if not DISCORD_TOKEN:
        LOGGER.error("Token de Discord no encontrado. Por favor, configura la variable de entorno DISCORD_TOKEN.")
        return
    await bot.start(DISCORD_TOKEN)

# Runner:
if __name__ == "__main__":
    LOGGER.info("Iniciando el bot...")
    asyncio.run(main())

