# Libs:
import time
from discord.ext import commands
from config.utils import get_game_info, get_game_weight, get_game_requirements
from config.config import PIVIGAMES_URL, LOGGER
from admin.manager import save_data

# Class GameCommands:
class GameCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Func Games:
    @commands.command()
    async def games(self, ctx):
        LOGGER.info("Comando 'games' invocado.")
        games = await get_game_info(PIVIGAMES_URL)
        if games:
            for title, link in games:
                weight = await get_game_weight(link)
                await ctx.send(f"Titulo: {title}\nEnlace: {link}\nPeso: {weight}")
        else:
            await ctx.send("No se encontraron juegos.")
        LOGGER.info(f"Comando 'games' completado. Juegos encontrados: {len(games)}")

    # Func for get requirements of all games:
    @commands.command()
    async def games_r(self, ctx):
        LOGGER.info("Comando 'games_r' invocado.")
        games = await get_game_info(PIVIGAMES_URL)
        if games:
            for title, link in games:
                requirements = await get_game_requirements(link)
                await ctx.send(f"{requirements}\n")
        else:
            await ctx.send("No se encontraron juegos.")
        LOGGER.info(f"Comando 'games_r' completado. Juegos encontrados: {len(games)}")

    # Func for find a game in Pivigames:
    @commands.command()
    async def find(self, ctx, *, game_name):
        LOGGER.info(f"Comando 'find' invocado con búsqueda: {game_name}")
        game_name_query = game_name.strip().replace(" ", "+")
        search_url = f"{PIVIGAMES_URL}?s={game_name_query}"
        games = await get_game_info(search_url)

        if games:
            message = f"Resultados de la búsqueda para **{game_name}**:\n"
            for title, link in games:
                message += f"Titulo: {title}\nEnlace: `{link}`\n\n"
            await ctx.send(message)
        else:
            await ctx.send(f"No se encontraron resultados para la búsqueda: **{game_name}**")
        LOGGER.info(f"Comando 'find' completado. Resultados encontrados: {len(games)}")

    # Func for get Requirements of Specific Game:
    @commands.command()
    async def requirements(self, ctx, link):
        LOGGER.info(f"Comando 'requirements' invocado para el enlace: {link}")
        req = await get_game_requirements(link)
        await ctx.send(req)
        LOGGER.info("Comando 'requirements' completado.")

    # Func for Track a specific Game:
    @commands.command()
    async def track(self, ctx, *, args):
        LOGGER.info(f"Comando 'track' invocado con argumentos: {args}")
        parts = args.split('tagg')
        if len(parts) != 2:
            await ctx.send("Formato incorrecto. Usa: @Pivimir track NOMBRE DEL JUEGO tagg @usuario")
            LOGGER.warning("Formato incorrecto en comando 'track'")
            return

        game_name, user_to_tag = map(str.strip, parts)
        self.bot.tracked_games[game_name.lower()] = {'user': user_to_tag, 'channel': ctx.channel.id}
        await ctx.send(f"¡Entendido! Te avisaré cuando {game_name} esté disponible, {user_to_tag}.")
        save_data(self.bot)
        LOGGER.info(f"Juego '{game_name}' agregado a la lista de seguimiento para el usuario {user_to_tag}")

    # Func for Activity Ping:
    @commands.command()
    async def ping(self, ctx):
        start_time = time.time()
        message = await ctx.send("Pong!")
        end_time = time.time()
        latency = round((end_time - start_time) * 1000)
        await message.edit(content=f"Pong! Latencia: {latency}ms")
        LOGGER.info(f"Comando 'ping' ejecutado. Latencia: {latency}ms")

    # Func for Print Commands:
    @commands.command()
    async def commands(self, ctx):
        LOGGER.info("Comando 'commands' invocado.")
        command_list = [
            "1. @Pivimir ping: Responde 'Pong' si Pivimir está online.",
            "2. @Pivimir commands: Muestra la lista de funciones del bot.",
            "3. @Pivimir games: Envía los juegos encontrados en el sitio web al canal configurado.",
            "4. @Pivimir games_r: Envía la lista actualizada de juegos con sus requisitos mínimos.",
            "5. @Pivimir find <nombre del juego>: Busca un juego por su nombre en el sitio web.",
            "6. @Pivimir requirements <enlace del juego>: Muestra los requisitos mínimos para ejecutar cada juego.",
            "7. @Pivimir track <nombre del juego> tagg @usuario: Rastrea un juego y notifica al usuario cuando esté disponible.",
            "8. @Pivimir set_channel: (Solo administradores) Configura el canal actual para las notificaciones.",
            "\nRecuerda que todos los juegos y datos recopilados de este bot, los encuentras en: https://pivigames.blog/"
        ]
        await ctx.send("Comandos disponibles para el bot:\n" + "\n".join(command_list))
        LOGGER.info("Lista de comandos enviada.")

# Func for Setup BOT:
async def setup(bot):
    await bot.add_cog(GameCommands(bot))
