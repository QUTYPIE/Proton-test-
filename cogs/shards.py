import discord
import logging
from discord.ext import commands

logging.basicConfig(
    level=logging.INFO,
    format="\x1b[38;5;197m[\x1b[0m%(asctime)s\x1b[38;5;197m]\x1b[0m -> \x1b[38;5;197m%(message)s\x1b[0m",
    datefmt="%H:%M:%S",
)

class ready(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Colour.green()

    @commands.Cog.listener()
    async def on_shard_ready(self, shard_id):
        logging.info("Shard #%s is ready" % (shard_id))

    @commands.Cog.listener()
    async def on_shard_connect(self, shard_id):
        logging.info("Shard #%s has connected" % (shard_id))

    @commands.Cog.listener()
    async def on_shard_disconnect(self, shard_id):
        logging.info("Shard #%s has disconnected" % (shard_id))

    @commands.Cog.listener()
    async def on_shard_resume(self, shard_id):
        logging.info("Shard #%s has resumed" % (shard_id))


async def setup(bot):
  await bot.add_cog(ready(bot))