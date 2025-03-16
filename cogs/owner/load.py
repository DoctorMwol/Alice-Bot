from discord import Object
from discord.app_commands import command
from discord.ext.commands import Cog

class LoadCog(Cog):
    def __init__(self, bot):
        self.bot = bot
    @command(name='load', description='Recarrega uma extensão (cog).')
    async def load(self, interaction, extension: str):
        """Comando para carregar uma extensão (cog)."""
        
        app_info = await self.bot.application_info()
        self.bot_owner_id = app_info.owner.id
        
        if interaction.user.id != self.bot.owner_id:
            return await interaction.response.send_message("Você não tem permissão para usar este comando!", ephemeral=True)
        try:
            await self.bot.unload_extension(extension)
            await interaction.response.send_message(f'Cog `{extension}` carregada com sucesso!', ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f'Ocorreu um erro ao carregar o cog `{extension}`: {e}', ephemeral=True)

    @Cog.listener()
    async def on_ready(self):
        print('    Load is ready!')

# Setup do cog
async def setup(bot):
    await bot.add_cog(
        LoadCog(bot),
        guilds=[Object(id=1236043718709088256)]
    )
