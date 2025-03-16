from discord import Member, Embed, User, Object, Interaction
from discord.app_commands import command, describe, checks, AppCommandError, MissingPermissions
from discord.ext.commands import Cog, Bot
from typing import Optional

class Kick(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @command(
        name='kick',
        description='kicka um usuário para fora do servidor!'
    )

    @describe(
        user='Selecione o úsuario que deseja kickar!',
        reason='Qual foi sua razão para kickar o usuário'
    )

    @checks.has_permissions(
        kick_members=True
    )
    
    async def _kick(
        self,
        interaction: Interaction,
        user: Member,
        reason: Optional[str] = 'Nenhum motivo aparente.'):
            if interaction.user == user:
                await interaction.response.send_message('Você não pode kickar você mesmo imbecil!', ephemeral=True)
            else:
                await print(user.email)
                await user.kick()
                await interaction.response.send_message(f'{user}({user.id}) foi kickado com sucesso!\nRazão: ``{reason}``')
        
    @_kick.error
    async def _kickError(
        self,
        interaction: Interaction,
        error: AppCommandError):
            if isinstance(error, MissingPermissions):
                await interaction.response.send_message('Você não ter permissão para kickar esse usuário!', ephemeral=True)
            else:
                await interaction.response.send_message('Ei! Você não pode kickar... Não consigo nem acreditar que vc tentou...', ephemeral=True)

    @Cog.listener()
    async def on_ready(self):
        print('    Kick is ready!')

async def setup(bot: Bot) -> None:
    await bot.add_cog(
        Kick(bot),
        guilds = [Object(id=1236043718709088256)])