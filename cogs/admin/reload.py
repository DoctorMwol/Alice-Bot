from discord import Object
from discord.app_commands import command
from discord.ext.commands import Cog

class ReloadCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='reload', description='Recarrega uma extensão (cog).')
    async def reload(self, interaction, extension: str):
        """Comando para recarregar uma extensão (cog)."""
        try:
            # Unload e load da extensão
            await self.bot.unload_extension(extension)
            await self.bot.load_extension(extension)
            await interaction.response.send_message(f'Cog `{extension}` recarregado com sucesso!', ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f'Ocorreu um erro ao recarregar o cog `{extension}`: {e}', ephemeral=True)

    @Cog.listener()
    async def on_ready(self):
        print('    Reload is ready!')

# Setup do cog
async def setup(bot):
    await bot.add_cog(ReloadCog(bot), guilds=[Object(id=1236043718709088256)])
