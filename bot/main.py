import os
import logging
from discord.ext import commands
from dotenv import load_dotenv


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:\
                                        %(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='[')


@bot.listen()
async def on_ready():
    print('join guild:')
    for g in bot.guilds:
        print(f'伺服器: {g}, ID: {g.id}', end='')
    print("\n")

# load all extension
files = ['commands', 'events']

print("loading extensions")
for f in files:
    print(f'searching file: {f}')
    for cog in os.listdir(f'cog/{f}'):
        if cog.endswith('.py'):
            name = cog[:-3]
            bot.load_extension(f'cog.{f}.{name}')
            print(f"{name}: loaded")
print("All Cog loaded")

if __name__ == "__main__":
    load_dotenv()
    bot.run(os.getenv("TOKEN"))
