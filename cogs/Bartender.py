import traceback
import requests as req
import random as r
from discord.ext import commands
from models.Drink import Drink

DRINK_URL = 'https://www.thecocktaildb.com/api/json/v1/1/'
FILTER_TYPES = ['a','alcoholic','bourbon','brandy','cognac','gin', 'na','nonalcoholic','rum','scotch','tequila','vodka','whiskey','wine']

BARTENDER_DESCRIPTION = 'Used to provide a delicious, sensual drink.'
DRINK_DESCRIPTION = 'Get a nice, refreshing drink from the Bartender'
DRINK_USAGE = '--> Gets a random drink\n.drink a | alcoholic --> Gets an alcoholic drink\n.drink na | nonalcoholic --> gets a nonalcoholic drink\n.drink [bourbon,brandy,cognac,gin,rum,scotch,tequila,vodka,whiskey,wine] --> Gets an alcoholic beverage of the given type'
class Bartender(commands.Cog, name='Bartender', description=BARTENDER_DESCRIPTION):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='drink', description=DRINK_DESCRIPTION, usage=DRINK_USAGE)
    async def drink(self, ctx, *args):
        if not args:
            random_drink_url = DRINK_URL + 'random.php'
            drink = await self.get_drink(ctx, random_drink_url)
            await ctx.send(embed=drink.embed)
            return
            
        if len(args) > 1:
            await ctx.send(f'There can only be one argument allow for this command, master.')
            return

        arg = args[0].lower()
        if arg in FILTER_TYPES:
            filter_response = self.get_drink_url_from_args(DRINK_URL, arg)
            if(filter_response['success'] == True):
                drink = await self.get_drink(ctx, filter_response["filter_url"])
                await ctx.send(embed = drink.embed)
            else:
                error = filter_response['error']
                await ctx.send(f'Master, something went wrong with the request: \n{error}')
        else:
            message = f"'{arg}' is not a valid argument - Better check your argument there, master."
            chance = r.randint(1,100)
            if chance > 80:
                message += ' (Filth...)'
            await ctx.send(message)
            return

#HELPER FUNCTIONS
    async def get_drink(self, ctx:commands.Context, filter_url:str) -> Drink:
        try:
            res = req.get(filter_url)
            res.raise_for_status()
        except req.HTTPError as ex:
            traceback.print_exc()
            await ctx.send(f'Master, something went wrong with the request: \n{ex}')

        json = res.json()
        drink = Drink(json['drinks'][0])
        return drink

    def get_drink_url_from_args(self, DRINK_URL:str, arg:str) -> str:
        if arg == 'a' or arg == 'alcoholic': filter = 'filter.php?a=Alcoholic' 
        elif arg == 'na' or arg == 'nonalcoholic': filter = 'filter.php?a=Non_Alcoholic'
        else: filter = f'filter.php?i={arg}'

        resolved_url = self._get_drink_lookup_url(DRINK_URL, filter)
        return resolved_url

    def _get_drink_lookup_url(self, DRINK_URL, filter) -> str:
        filter_url = DRINK_URL + filter
        try:
            drink_list = req.get(filter_url).json()['drinks']
            drink_id = r.choice(drink_list)['idDrink']
        except req.HTTPError as ex:
            return {
                "success": False,
                "error": ex
            }
        
        return {
            "success": True,
            "filter_url": DRINK_URL + f'lookup.php?i={drink_id}'
            }


def setup(bot):
    bot.add_cog(Bartender(bot))