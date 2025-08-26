import traceback
from discord.ext import commands
from imp_bot.models.drink import Drink
from util import utility

class Bartender(commands.Cog, name='Bartender', description='Bartender serves up a random alcoholic or nonalcoholic drink in an embedded fashion!'):
    def __init__(self, bot):
        self.bot = bot
        self._request = utility.Request
        self._sanitizer = utility.DrinkJsonSanitizer
        self._embedder = utility.DrinkEmbedder
        self._formatter = utility.DrinkFormatter
    
    @commands.command(name='drink', description='Get a nice, freshing drink from the Bartender',aliases=['drinks', 'cocktail', 'cocktails'])
    async def drink(self, ctx):
        print("Getting Drink")
        try:
            drink_json = self._request().get_drink_json()
            drink = Drink(drink_json,self._sanitizer, self._formatter, self._embedder)
            await ctx.send(embed = drink.embed)
        except Exception as ex:
            traceback.print_exc()
            await ctx.send(f'Ayo, your code is wack.\n Error: {ex}')
    
async def setup(bot):
    await bot.add_cog(Bartender(bot))