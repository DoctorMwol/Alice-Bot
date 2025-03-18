from discord import Member, Embed, User, Object, Interaction
from discord.app_commands import command, describe, checks, AppCommandError, MissingPermissions
from discord.ext.commands import Cog, Bot
from typing import Optional

class Unban(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @command(
        name='unban',
        description='Permite o usuário voltar o céu!'
    )

    @describe(
        user='Selecione o usuário que deseja desbanir!',
    )

    @checks.has_permissions(
        ban_members=True
    )

    async def _unban(
        self,
        interaction: Interaction,
        user: User,):
            #async for entry in interaction.guild.bans(limit=150):
            #    print(entry.user, entry.reason)
            
            if interaction.client.user.id == user.id:
                return await interaction.response.send_message('Você ta louco? Tentando me desbanir sendo que nem estou banida...', ephemeral=True)
            
            embed = Embed(
                title='Sucesso!',
                description=f'{user}({user.id}) foi desbanido com sucesso!\n**Razão do banimento**: ``````',
                colour= 0x313338
            )
            embed.set_thumbnail(url=user.avatar)
            if interaction.user == user:
                await interaction.response.send_message('Mano! você não foi banido, então para querer ser desbanido!', ephemeral=True)
            else:
                await interaction.guild.unban(user)
                await interaction.response.send_message(embed=embed)
    
    @_unban.error
    async def _unbanError(
        self,
        interaction: Interaction,
        error: AppCommandError):
            if isinstance(error, MissingPermissions):
                await interaction.response.send_message('Você não ter permissão para desbanir esse usuário!', ephemeral=True)
            else:
                await interaction.response.send_message('Este usuário não foi banido!', ephemeral=True)

    @Cog.listener()
    async def on_ready(self):
        print('    Unban is ready!')

async def setup(bot: Bot) -> None:
    await bot.add_cog(
        Unban(bot),
        guilds = [Object(id=1236043718709088256)])