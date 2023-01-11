import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from helpers import checks
from utils.checks import getConfig, updateConfig


class Welcomer(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.color = 0x01f5b6

    @commands.Cog.listener()
    async def on_member_join(self, user):
        try:
            guild = user.guild
            data = getConfig(user.guild.id)

            if data["wen"] != True:
                return 
            if data["message"] == None:
                return
            if data["channel"] == None:
                return

            channel = self.client.get_channel(data["channel"])
            message = data["message"]
            if "{user.id}" in message:
                    message = message.replace("{user.id}", "%s" % (user.id))

            if "{user.mention}" in message:
                message = message.replace("{user.mention}", "%s" % (user.mention))

            if "{user.tag}" in message:
                message = message.replace("{user.tag}", "%s" % (user.discriminator))

            if "{user.name}" in message:
                message = message.replace("{user.name}", "%s" % (user.name))
                
            if "{user.avatar}" in message:
                message = message.replace("{user.avatar}", "%s" % (user.avatar_url))

            if "{server.name}" in message:
                message = message.replace("{server.name}", "%s" % (user.guild.name))
                
            if "{server.membercount}" in message:
                message = message.replace("{server.membercount}", "%s" % (user.guild.member_count))
                
            if "{server.icon}" in message:
                message = message.replace("{server.icon}", "%s" % (user.guild.icon_url))
            
            await channel.send(message)
        except Exception:
            pass
      
async def setup(client):
    await client.add_cog(Welcomer(client))
