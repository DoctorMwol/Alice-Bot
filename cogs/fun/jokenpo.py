from discord import Interaction, Object
from discord.app_commands import command, describe, choices
from discord.app_commands import Choice
from discord.ext.commands import Cog, Bot
from random import choice
from db.database import check_and_create_user, update_score, get_user_stats


class Fun(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @command(
        name='jokenpo',
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
            update_score(user_id, 0, 0, 1, 1)
        elif rule[move][play.index(bot_move)] == 'v':
            update_score(user_id, 1, 0, 0, 3)
        else:
            update_score(user_id, 0, 1, 0, 1)
        
        
        
        score = get_user_stats(user_id)
        
        await interaction.response.send_message(f'Você jogou {play[move]} e joguei {bot_move}. ' + text[rule[move][play.index(bot_move)]] + '\n' + f'Você tem {score['wins']} vitórias, {score['losses']} derrotas e {score['draws']} empates. TOTAL: {score['total_games']} pontos.')

    @Cog.listener()
    async def on_ready(self):
        print('    Jokenpo funcion ready')
    
async def setup(bot: Bot) -> None:
    await bot.add_cog(
        Fun(bot),
        guilds=[Object(id=1236043718709088256)])