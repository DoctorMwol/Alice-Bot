import asyncio
from discord import Member, Embed, User, Object, Interaction, TextChannel
from discord.app_commands import command, describe, checks, AppCommandError, MissingPermissions
from discord.ext.commands import Cog, Bot, Group
from typing import Optional

class Cleanner(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(
        name="clean",
        description="Apaga um número específico de mensagens."
    )
    @describe(num="Número de mensagens a apagar (máximo: 100).")
    @checks.has_permissions(manage_messages=True)
    async def _clean(
        self,
        interaction: Interaction,
        num: Optional[int] = 10
    ):
        if not isinstance(interaction.channel, TextChannel):
            await interaction.response.send_message("Este comando só pode ser usado em canais de texto!", ephemeral=True)
            return

        num = min(max(num, 1), 100)
        await interaction.response.send_message(f"🧹 **|** Apagando {num} mensagens...", ephemeral=True)
        deleted = await interaction.channel.purge(limit=num, check=lambda m: m.author != interaction.client.user)
        
        await asyncio.sleep(5)
        await interaction.edit_original_response(content=f"🧹 **|** {len(deleted)} mensagens foram apagadas!")

    @Cog.listener()
    async def on_ready(self):
        print('    Clean is ready!')

async def setup(bot: Bot) -> None:
    await bot.add_cog(
        Cleanner(bot),
        guilds = [Object(id=1236043718709088256)])
