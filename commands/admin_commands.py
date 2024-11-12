# Libs:
from discord.ext import commands
from config.config import LOGGER
from admin.manager import save_data

# Class Administrator:
class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Func for Set Channel:
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_channel(self, ctx):
        self.bot.discord_channel = ctx.channel
        self.bot.channel_id = ctx.channel.id 
        await ctx.send(f"Canal '{ctx.channel.name}' configurado exitosamente para las notificaciones.")
        save_data(self.bot)
        LOGGER.info(f"Nuevo canal configurado: {ctx.channel.name}")

        game_tasks = self.bot.get_cog('GameTasks')
        if game_tasks:
            if not game_tasks.search_games.is_running():
                game_tasks.search_games.start()
            if not game_tasks.check_tracked_games.is_running():
                game_tasks.check_tracked_games.start()

# Func for Setup BOT:
async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
    
