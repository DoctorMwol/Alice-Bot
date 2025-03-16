from discord import Member, Embed, User, Object, Interaction
from discord.app_commands import command, describe, checks, AppCommandError, MissingPermissions
from discord.ext.commands import Cog, Bot, GroupCog
from typing import Optional

class User(GroupCog, name = 'user'):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    """Avatar"""

    @command(
        name='avatar',
        description='Mostra o seu avatar ou de outro usuário!'
    )
    @describe(
        user='O usuário que você deseja roubar...',
    )
    async def _avatar(
        self,
        interaction: Interaction,
        user: Optional[Member] = None,):

        if user is None:
            avatar_image = interaction.user.avatar
            name = interaction.user.name
        else:
            avatar_image = user.avatar
            name = user.name

        embed = Embed(
            title = f'🖼️ **{name}**',
            description = f'**Clique [aqui]({avatar_image.replace(size=2048)}) para baixar a imagem!**',
            color = 0x313338
            )
        embed.set_image(url=avatar_image)
        await interaction.response.send_message(embed=embed)
    
    """Banner"""
    
    @command(
        name='banner',
        description='Mostra o seu banner ou de outro usuário!'
    )
    @describe(
        user='O usuário que você deseja roubar...',
    )
    async def _banner(
        self, 
        interaction: Interaction,
        user: Optional[Member] = None,):

        if user == None:
            banner_image = interaction.user.banner
            user = interaction.user
        else:
            banner_image = user.banner
        
        if banner_image == None:
            await interaction.response.send_message(f'❌ **|** {user.mention} não tem um banner no perfil! Talvez ele não tenha Discord Nitro... Ou talvez ele só teve muita preguiça de colocar um banner bonitinho.', ephemeral=True)

        else:
            embed = Embed(
                title = f'🖼️ **{user.name}**',
                description = f'**Clique [aqui]({banner_image}) para baixar a imagem!**',
                color = 0x313338
                )
            embed.set_image(url=banner_image)
            await interaction.response.send_message(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        print('    User is ready!')
        

async def setup(bot: Bot) -> None:
    await bot.add_cog(
        User(bot),
        guilds = [Object(id=1236043718709088256)])