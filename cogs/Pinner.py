import traceback
from models.Pin import Pin
from discord.ext import commands
from util import Utility

class Pinner(commands.Cog, name='Pinner', description='Pinner allows you to make any message an embed and then pin it to the Pins channel.'):
    
    def __init__(self, bot):
        self.bot = bot
        self._pin = Pin
        self._embedder = Utility.PinEmbedder


    @commands.command(name='pin', description='Reply to a message with this command to pin it to the Pins channel', aliases=['pin, this'])
    async def pin(self, ctx):
        try:
            if not ctx.message.reference:
                await ctx.message.channel.send('You have to reply .pin to the message you want pinned.')
                return
            reply = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
            pin = self._pin(reply, self._embedder)
            pin_channel = self.bot.get_channel(872962501707456592)
            await pin_channel.send(embed=pin.embed)
            
            reactions = ['👍']
            for emoji in reactions: 
                await ctx.message.add_reaction(emoji)
            
        except Exception as ex:
            print(ex)
            traceback.print_exc()
            await ctx.message.channel.send(f'Ayo, your code is wack.\n Error: {ex}')
    
def setup(bot):
    bot.add_cog(Pinner(bot))