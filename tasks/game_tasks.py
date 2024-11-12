# Libs:
from discord.ext import tasks, commands
from config.config import LOGGER, PIVIGAMES_URL
from admin.manager import save_data
from config.utils import get_game_info, get_game_weight

# Class GameTasks:
class GameTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Func On Ready:
    @commands.Cog.listener()
    async def on_ready(self):
        LOGGER.info(f'Bot conectado como {self.bot.user}')
        if self.bot.channel_id:
            self.bot.discord_channel = self.bot.get_channel(self.bot.channel_id)
        else:
            self.bot.discord_channel = None

        if self.bot.discord_channel:
            LOGGER.info(f'Canal cargado: {self.bot.discord_channel.name}')
            self.search_games.start()
            self.check_tracked_games.start()
        else:
            LOGGER.warning('Canal no configurado. Usa el comando set_channel para configurar el canal.')

    # Func for Guild_Join_SRV:
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send("¡Hola a todos! Soy Pivimir-bot, desarrollado por @Devnis. Usa '@Pivimir set_channel' para configurar mi canal de interacción.")
                LOGGER.info(f'Bot se unió al servidor: {guild.name}')
                break

    # Func for Search Games:
    @tasks.loop(hours=12)
    async def search_games(self):
        if not self.bot.discord_channel:
            LOGGER.warning('Canal de Discord no configurado. No se pueden enviar juegos.')
            return

        LOGGER.info('Iniciando búsqueda de nuevos juegos...')
        games = await get_game_info(PIVIGAMES_URL)
        new_games = []

        for title, link in games:
            if title not in self.bot.prev_titles:
                weight = await get_game_weight(link)
                game_info = f"Título: {title}\nEnlace: {link}\nPeso: {weight}"
                new_games.append(game_info)
                self.bot.prev_titles.add(title)

        if new_games:
            LOGGER.info(f'Se encontraron {len(new_games)} nuevos juegos.')
            await self.bot.discord_channel.send("¡Encontré nuevos juegos en Pivigames! Aquí les dejo la lista actualizada:")
            for game in new_games:
                await self.bot.discord_channel.send(game)
            save_data(self.bot)
        else:
            LOGGER.info('No se encontraron nuevos juegos.')

    # Func for Check Tracked Games:
    @tasks.loop(hours=3)
    async def check_tracked_games(self):
        LOGGER.info("Iniciando verificación de juegos rastreados.")
        games = await get_game_info(PIVIGAMES_URL)
        for game_title, game_link in games:
            game_title_lower = game_title.lower()

            for tracked_game, track_info in list(self.bot.tracked_games.items()):
                tracked_game_words = set(tracked_game.split())
                game_words = set(game_title_lower.split())
                common_words = tracked_game_words.intersection(game_words)

                if len(common_words) >= 2:
                    user_to_tag = track_info['user']
                    channel = self.bot.get_channel(track_info['channel'])

                    if channel:
                        weight = await get_game_weight(game_link)
                        message = f"{user_to_tag}, ¡el juego que estabas esperando ya está disponible!\n"
                        message += f"Título: {game_title}\nEnlace: {game_link}\nPeso: {weight}"
                        await channel.send(message)
                        LOGGER.info(f"Notificación enviada para el juego '{game_title}' al usuario {user_to_tag}")
                    del self.bot.tracked_games[tracked_game]
                    save_data(self.bot)

        LOGGER.info("Verificación de juegos rastreados completada.")

# Fun for Setup BOT:
async def setup(bot):
    await bot.add_cog(GameTasks(bot))
