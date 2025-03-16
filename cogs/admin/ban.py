from discord import Member, Embed, User, Object, Interaction
from discord.app_commands import command, describe, checks, AppCommandError, MissingPermissions
from discord.ext.commands import Cog, Bot
from typing import Optional

class Ban(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @command(
        name='ban',
        description='Joga o usuário selecionado no inferno!'
    )

    @describe(
        user='Selecione o usuário que deseja banir!',
        reason='Qual foi sua razão para banir o usuário'
    )

    @checks.has_permissions(
        ban_members=True
    )

    async def _ban(
        self,
        interaction: Interaction,
        user: Member,
        reason: Optional[str] = 'Nenhum motivo aparente'):

            embed = Embed(
                title='Sucesso!',
                description=f'{user}({user.id}) foi banido com sucesso!\n**Razão**: ```{reason}```',
                colour= 0x36393f
            )
            embed.set_thumbnail(url=user.avatar)
            
            if interaction.user == user:
                await interaction.response.send_message('Você não pode banir você mesmo!', ephemeral=True)
            else:
                await user.ban(reason=reason)
                await interaction.response.send_message(embed=embed)
    
    @_ban.error
    async def _banError(
        self,
        interaction: Interaction,
        error: AppCommandError):
            if isinstance(error, MissingPermissions):
                await interaction.response.send_message('Você não ter permissão para banir esse usuário!', ephemeral=True)
            else:
                await interaction.response.send_message('Ei! Você não pode banir o bot!', ephemeral=True)


    @Cog.listener()
    async def on_ready(self):
        print('    Ban is ready!')

async def setup(bot: Bot) -> None:
    await bot.add_cog(
        Ban(bot),
        guilds=[Object(id=1236043718709088256)])