import traceback
from discord.ext import commands
from models.Drink import Drink
from util import Utility

class Music(commands.Cog, name='Jukebox', description='Used to automatically play environmental songs and ambient music'):

    def __init__(self, bot):
        self.bot = bot
        self._links = {
            "session-start": 'https://www.youtube.com/watch?v=fIuO3RpMvHg',
            "battle-music": ['https://www.youtube.com/watch?v=lAGm9MTyRJ8'],
            "desert": ['https://www.youtube.com/watch?v=svdbNil4fAI'],
            "town-center": ['https://www.youtube.com/watch?v=NeOg8iCFfTA'],
            "bar": ['https://www.youtube.com/watch?v=_4OfDN6X9oc'],
            "docks": ['https://www.youtube.com/watch?v=t0AmfPQMs4k'],
            "cave": ['https://www.youtube.com/watch?v=kxqJuc1HHbg&t=397s']
        }
    
    @commands.command(name='music', description='Plays any of the following songs:\nBattle Music')
    async def music(self, ctx: commands.Context, *args):
        url = None
        is_dm = False
        for role in ctx.author.roles:
            if role.id == Utility.Roles.GOD_OF_THE_MULTIVERSE.value:
                is_dm = True

        if(not is_dm):
            await ctx.channel.send("You do not have the permissions to do this, peasant.")

        if(len(args) == 1):
            url = self._url_factory(args[0])

        if(url is None):
            await ctx.channel.send("That's not a valid theme music, master. Do try again.")

        else:
            await ctx.channel.send(f"Here you are, Master:\n!play {url}")


    
    def _url_factory(self, theme):
        print(theme)
        if(theme == 'session-start'):
            return self._links['session-start']

        elif(theme == 'battle-music'):
            return self._links['battle-music'][0]

        elif(theme == 'desert'):
            return self._links['desert'][0]

        elif(theme == 'town-center'):
            return self._links['town-center'][0]

        elif(theme == 'bar'):
            return self._links['bar'][0]

        elif(theme == 'docks'):
            return self._links['docks'][0]

        elif(theme == 'cave'):
            return self._links['cave'][0]
    
        else:
            return None


def setup(bot):
    bot.add_cog(Music(bot))


