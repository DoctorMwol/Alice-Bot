from discord.ext.commands import Cog
from discord import Object
from discord.app_commands import command, AppCommandError, checks
from discord.app_commands.errors import CommandOnCooldown
from discord import Interaction
class Say(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(name='say', description='Faz o bot falar algo')
    @checks.cooldown(1, 10.0)
    async def _say(self, interaction: Interaction, message: str):
        await interaction.response.send_message(message)
    @_say.error
    async def _unbanError(
        self,
        interaction: Interaction,
        error: AppCommandError):
        if isinstance(error, CommandOnCooldown):
            await interaction.response.send_message(f'Você está em cooldown! Tente novamente em {error.retry_after:.2f} segundos.', ephemeral=True)


    @Cog.listener()
    async def on_ready(self):
        print('    Say is ready!')

async def setup(bot):
    await bot.add_cog(
        Say(bot), 
        guilds=[Object(id=1236043718709088256)])