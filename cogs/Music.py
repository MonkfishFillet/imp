import traceback
from discord.ext import commands
from models.Drink import Drink
from util import Utility

class Music(commands.Cog, name='Jukebox', description='Used to automatically play environmental songs and ambient music'):

    def __init__(self, bot):
        self.bot = bot
        self._request = Utility.Request()
        self._music_links = {}
    
    @commands.command(name='music', description='Plays any of the following songs:\nBattle Music')
    async def music(self, ctx, *args):
         if(len(args) > 1):
             url = self._request.get_url(url_name='battle_music')
             channel = self.bot.get_channel(834485620843085884)

             await channel.send('.play ' + url)

    
def setup(bot):
    bot.add_cog(Music(bot))

