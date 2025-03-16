import os
from glob import glob
from discord import Object
from discord.app_commands import command  # Importando o decorador correto
from discord.ext.commands import Cog

class ReloadCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='reload', description='Recarrega uma extensão (cog) ou todas as cogs de uma pasta.')
    async def _reload(self, interaction, extension: str = None):
        """Comando para recarregar uma extensão (cog), todas as cogs de uma pasta ou todas as cogs carregadas."""
        
        app_info = await self.bot.application_info()
        self.bot_owner_id = app_info.owner.id
        
        # Se o usuário não for o dono do bot, retorna um erro
        if interaction.user.id != self.bot_owner_id:
            return await interaction.response.send_message("Você não tem permissão para usar este comando!", ephemeral=True)

        # Se não fornecer a extensão nem pasta
        if extension is None:
            return await interaction.response.send_message("Você precisa fornecer uma extensão ou uma pasta.", ephemeral=True)
        
        all_reloaded = []  # Lista para armazenar as cogs recarregadas
        response_message = ""  # Mensagem que será enviada no final

        if extension.lower() == 'all':  # Caso 'all', recarrega todas as cogs carregadas
            for cog_name in list(self.bot.extensions):  # Usa o nome do arquivo da extensão, não a classe
                try:
                    await self.bot.unload_extension(cog_name)
                    await self.bot.load_extension(cog_name)
                    cog_name = cog_name.split('.')[-1].capitalize()
                    all_reloaded.append(cog_name)  # Adiciona o nome da cog à lista
                except Exception as e:
                    print(f'Error reloading {cog_name}: {e}')
            
            response_message = f"```Cogs reloaded:\n{', '.join(all_reloaded)}```"

        elif '.' in extension:  # Se for o nome de uma extensão (cog), recarrega uma COG específica
            try:
                await self.bot.unload_extension(extension)
                await self.bot.load_extension(extension)
                response_message = f'Cog `{extension}` recarregado com sucesso!'
            except Exception as e:
                response_message = f'Ocorreu um erro ao recarregar o cog `{extension}`: {e}'
        
        else:  # Se for uma pasta, recarrega todas as COGs dessa pasta
            folder_path = f'./cogs/{extension}'
            if not os.path.exists(folder_path):
                response_message = f'Pasta `{extension}` não encontrada!'
            else:
                cogs_to_reload = [path.split('\\')[-1][:-3] for path in glob(f'{folder_path}/*.py')]
                if not cogs_to_reload:
                    response_message = f'Nenhuma COG encontrada na pasta `{extension}`.'
                else:
                    for cog in cogs_to_reload:
                        try:
                            await self.bot.unload_extension(f'cogs.{extension}.{cog}')
                            await self.bot.load_extension(f'cogs.{extension}.{cog}')
                            cog = cog.split('.')[-1].capitalize()
                            all_reloaded.append(cog)  # Adiciona o nome da cog à lista
                        except Exception as e:
                            print(f'Error reloading {cog}: {e}')
                    
                    response_message = f"```Cogs reloaded:\n{', '.join(all_reloaded)}```"
        
        # Envia a mensagem final, garantindo que seja feita apenas uma vez
        if response_message:
            await interaction.response.send_message(response_message, ephemeral=True)

    @Cog.listener()
    async def on_ready(self):
        print('    Reload is ready!')

# Setup do cog
async def setup(bot):
    await bot.add_cog(ReloadCog(bot), guilds=[Object(id=1236043718709088256)])
