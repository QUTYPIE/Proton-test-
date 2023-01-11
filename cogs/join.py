import os
import discord
import aiohttp
from discord.ext import commands, tasks
from discord.colour import Color
import json
import random
from utils.checks import getConfig, updateConfig

#https://cdn.discordapp.com/attachments/1027593292642275418/1028516662221226024/Proton.png

class Join(commands.Cog):
    def __init__(self, client):
        self.client = client

    

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
          data = getConfig(guild.id)
          key = "".join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") for _ in range(16))
          data['backupkey'] = key
          updateConfig(guild.id, data)
          embed = discord.Embed(
            description="Best Security Bot",
            color=0x01f5b6
          )
          embed.set_author(
            name="Proton"
          )
          embed.add_field(
            name="Thanks For Adding Me",
            value=f"Hey {guild.owner.mention}, Thanks for using me as your server protection bot, i will try my best with my powerful antinuke features to stop any nuke attempts on your server, but there are some steps you should be doing before it can work, you can get more info using the `/help` command.",
            inline=False
          ) 
          embed.add_field(
            name=f"Backup Key - `{key}`",
            value="You must keep this key safe this will be usefull when you lost ownership of server this key will help you to recover bot owner in server",
            inline=False
          ) 
          embed.set_thumbnail(
            url = "https://cdn.discordapp.com/attachments/1027593292642275418/1028516662221226024/Proton.png"
          )  
          embed.set_footer(
            text="Made with 💖 by Proton Developement"
          )
          await guild.owner.send(embed=embed)

    @commands.Cog.listener(name="on_guild_join")
    async def ffoo(self, guild):
      embed = discord.Embed(title="Proton | New Server", color=0x01f5b6)
      embed.add_field(name="Name", value=str(guild.name), inline=False)
      rope = [inv for inv in await guild.invites() if inv.max_age == 0 and inv.max_uses == 0]
      me = self.client.get_channel(1034354975691771904)
      embed.add_field(name="Member Count", value=f"{guild.member_count} Member(s)", inline=False)
      embed.add_field(name="Owner", value=f"[{guild.owner}](https://discord.com/users/{guild.owner_id})", inline=False)
      embed.add_field(name="Invite", value=f"[here]({rope[0]})" if rope else "No Pre-Made Invite Found", inline=False)
      await me.send(embed=embed)  

    @commands.Cog.listener(name="on_guild_remove")
    async def on_g_remove(self, guild):
      idk = self.client.get_channel(1034355961986568192)
      embed = discord.Embed(title="Proton | Removed", color=0x01f5b6)
      embed.add_field(name="Name", value=str(guild.name), inline=False)
      embed.add_field(name="Member Count", value=f"{guild.member_count} Member(s)", inline=False)
      embed.add_field(name="Owner", value=f"[{guild.owner}](https://discord.com/users/{guild.owner_id})", inline=False)
      await idk.send(embed=embed)
  
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
      with open("database/config.json", "r") as f:
          data = json.load(f)

      del data["guilds"][str(guild.id)]

      with open("database/config.json", "w") as f:
          json.dump(data, f)                 
                


async def setup(client):
	await client.add_cog(Join(client))