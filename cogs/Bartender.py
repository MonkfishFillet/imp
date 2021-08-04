import requests
import traceback
from discord.ext import commands
from models.Drink import Drink
from util import Utility

class Bartender(commands.Cog, name='Bartender', description='Used to provide any bud with a delicious, sensual drink'):

    def __init__(self, bot):
        self.bot = bot
        self._request = Utility.Request
        self._sanitizer = Utility.DrinkJsonSanitizer
        self._embedder = Utility.DrinkEmbedder
        self._formatter = Utility.DrinkFormatter
    
    @commands.command(name='drink', description='Get a nice, freshing drink from the Bartender',aliases=['drinks', 'cocktail', 'cocktails'])
    async def drink(self, ctx):
        try:
            drink_json = self._request().get_drink_json()
            drink = Drink(drink_json,self._sanitizer, self._formatter, self._embedder)
            await ctx.send(embed = drink.embed)
        except Exception as ex:
            traceback.print_exc()
            await ctx.send(f'Ayo, your code is wack.\n Error: {ex}')
    
def setup(bot):
    bot.add_cog(Bartender(bot))