import os
import asyncio
from dotenv import load_dotenv
from discord import Intents
from discord.ext.commands import Bot, Context
from imp_bot import __version__


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
COGS_DIR = "./src/imp_bot/cogs"
FILES = [
    file
    for file in os.listdir(COGS_DIR)
    if all([file.endswith(".py"), "__init__.py" not in file])
]


async def load_cogs(bot: Bot):
    for file in FILES:
        await bot.load_extension(f"imp_bot.cogs.{file[:-3]}")
        print(f"{file[:-3]} extension loaded")


async def unload_cogs(bot: Bot):
    for file in FILES:
        await bot.unload_extension(f"imp_bot.cogs.{file[:-3]}")
        print(f"{file[:-3]} extension unloaded")


async def _construct_bot():
    intents = Intents.default()
    intents.message_content = True
    bot = Bot(command_prefix=".", intents=intents)

    @bot.command(
        name="refresh",
        description="Reloads all cogs",
        aliases=["reload"],
        hidden=True,
    )
    async def refresh(ctx: Context):
        print("Reloading Cogs...\n")
        await unload_cogs(bot)
        await load_cogs(bot)
        print("Cogs reloaded successfully")
        await ctx.message.add_reaction("👍")


    @bot.event
    async def on_ready():
        print(f"Imp v{__version__} is now running.")
        print(f"{bot.user} is ready to serve, Master.")
        
    return bot


async def run_bot():
    bot = await _construct_bot()
    await load_cogs(bot)
    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(run_bot())
