import traceback
from models import Party, Character
from util import Utility
from discord.ext import commands

class Party(commands.Cog, name='Party', description='Provides information about party and character statistics'):
    
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='party', description='')
    async def party(self, ctx: commands.Context, *args):
        try:
            pass
            
        except Exception as ex:
            pass
    
def setup(bot):
    bot.add_cog(Party(bot))