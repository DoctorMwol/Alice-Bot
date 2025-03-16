from discord import Interaction, Object, Embed
from discord.app_commands import Choice, command, describe, choices
from discord.ext.commands import Cog, Bot, GroupCog
from random import choice
from db.database import check_and_create_user, update_score, get_user_stats


class Jokenpo(GroupCog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()
    
    @command(
        name='game',
        description='Jogue jokenpo contra o bot'
    )
    
    @describe(
        move='Seu movimento'
    )
    
    @choices(move=[
        Choice(name='Pedra!', value=0),
        Choice(name='Papel!', value=1),
        Choice(name='Tesoura!', value=2)
    ])
    
    async def _jokenpo(
        self,
        interaction: Interaction,
        move: int
    ) -> None:
        
        play = ('pedra', 'papel', 'tesoura')
        rule = (('e', 'd', 'v'),
                ('v', 'e', 'd'),
                ('d', 'v', 'e'))
        
        text = {'e': 'Empatou!',
                'v': 'Parabéns você ganhou!',
                'd': 'Você perdeu!'}
        
        user_id = interaction.user.id
        bot_move = choice(play)
        
        check_and_create_user(user_id)
        
        if rule[move][play.index(bot_move)] == 'e':
            update_score(user_id, wins=0, losses=0, draws=1,)
        elif rule[move][play.index(bot_move)] == 'v':
            update_score(user_id, wins=1, losses=0, draws=0)
        else:
            update_score(user_id, wins=0, losses=1, draws=0)
        
        
        await interaction.response.send_message(f'Você jogou {play[move]} e joguei {bot_move}. ' + text[rule[move][play.index(bot_move)]])

    @command(
        name='score',
        description='Veja seu score'
    )
    async def _score(
        self,
        interaction: Interaction
    ) -> None:
        user_id = interaction.user.id
        score = get_user_stats(user_id)
        
        embed = Embed(
            title='Seu score',
            color=0x313338
        )
        
        embed.add_field(
            name='Vitórias',
            value=score['wins'],
            inline=True
        )

        embed.add_field(
            name='Derrotas',
            value=score['losses'],
            inline=True
        )

        embed.add_field(
            name='Empates',
            value=score['draws'],
            inline=True
        )
        embed.add_field(
            name='Total',
            value=score['total_games'],
            inline=True
        )
        embed.set_footer(
            text=f'ID: {user_id}'
        )
        embed.set_thumbnail(
            url=interaction.user.avatar.url
        )

        await interaction.response.send_message(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        print('    Jokenpo  is ready!')
    
async def setup(bot: Bot) -> None:
    await bot.add_cog(
        Jokenpo(bot),
        guilds=[Object(id=1236043718709088256)])