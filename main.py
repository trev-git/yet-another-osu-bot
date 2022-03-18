import discord
from discord.ext import commands

initial_extensions = ['cogs.osu_commands']
bot = commands.Bot(command_prefix='#')

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game('osu!'))

bot.run('')
