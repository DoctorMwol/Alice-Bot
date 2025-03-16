import os
from glob import glob
from dotenv import load_dotenv

from discord import Intents, Object
from discord.ext.commands import Bot as BotBase

load_dotenv()

FOLDERS = os.listdir('./cogs')

class Bot(BotBase):

    def __init__(self):
        super().__init__(
            command_prefix='!',
            owner_ids=[int(os.getenv("OWNER_ID"))],
            case_insensitive=True,
            intents=Intents.all(),
            application_id=1189392933783347300,
        )

    async def setup_hook(self):
        print('Loading Cogs...')
        for folder in FOLDERS:
            cogs = [path.split('\\')[-1][:-3] for path in glob(f'./cogs/{folder}/*.py')]
            print(f'Module {folder} loading...')
            for cog in cogs:
                await self.load_extension(f'cogs.{folder}.{cog}')
                print(f'    {cog.capitalize()} loading!')
        print('Cogs loaded!')

        await self.tree.sync(guild=Object(id=1236043718709088256))  # await self.tree.sync()
        print('Slash commands globally synced!')

    def run(self):
        super().run(os.getenv("TOKEN"))

    async def on_connect(self):
        print(f'{self.user.name} connected')

    async def on_disconnect(self):
        print(f'{self.user.name} disconnected')

    async def on_ready(self):
        print(f'{self.user.name} ready')

bot = Bot()
bot.run()
