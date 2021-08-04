import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='.')

#region Cogs
'''
    Cog Functions & Commands
'''
def load_cogs():
    for files in os.listdir('./cogs'):
        if files.endswith('.py'):              
            bot.load_extension(f'cogs.{files[:-3]}')
            print(f'{files[:-3]} extension loaded')

def unload_cogs():
    for files in os.listdir('./cogs'):
        if files.endswith('.py'):              
            bot.unload_extension(f'cogs.{files[:-3]}')
            print(f'{files[:-3]} extension unloaded')

@bot.command(name='refresh', description='Reloads all cogs', alais=['refresh, reload'])
async def refresh(ctx: commands.Context):
    print('Reloading Cogs...\n')
    unload_cogs()
    load_cogs()
    print('Cogs reloaded successfully')
    reactions = ['👍']
    for emoji in reactions: 
        await ctx.message.add_reaction(emoji)
    
#endregion

@bot.event
async def on_ready():
    print(f'{bot.user} is ready to serve, Master.')


load_cogs()
bot.run(TOKEN)