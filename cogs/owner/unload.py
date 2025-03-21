from discord import Object
from discord.app_commands import command
from discord.ext.commands import Cog

class UnloadCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='unload', description='Descarrega uma extensão (cog).')
    async def _unload(self, interaction, extension: str):
        """Comando para descarregar uma extensão (cog)."""
        
        app_info = await self.bot.application_info()
        self.bot_owner_id = app_info.owner.id
        
        if interaction.user.id != self.bot.owner_id:
            return await interaction.response.send_message("Você não tem permissão para usar este comando!", ephemeral=True)
        try:
            await self.bot.unload_extension(extension)
            await interaction.response.send_message(f'Cog `{extension}` descarregada com sucesso!', ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f'Ocorreu um erro ao descarregar o cog `{extension}`: {e}', ephemeral=True)

    @Cog.listener()
    async def on_ready(self):
        print('    Unload is ready!')

# Setup do cog
async def setup(bot):
    await bot.add_cog(
        UnloadCog(bot),
        guilds=[Object(id=1236043718709088256)]
    )
