import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from helpers import checks
from utils.checks import getConfig, updateConfig, guild_owner_only



class Security(commands.Cog, name="Security"):
    def __init__(self, bot):
        self.bot = bot

    def help_custom(self):
        emoji = '<:security:1040651933972705341>'
        label = "Security"
        description = "Shows Security COmmands"
        return emoji, label, description

    @commands.hybrid_group(
        name="antinuke",
        description="shows antinuke configuration/instructions",
    )  
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    async def antinuke(self, context: Context) -> None:
      g = getConfig(context.guild.id)
      wlrole = g['wlrole']   
      channel = g['log_channel']
      embed = discord.Embed(
            description=f"Antinuke Config For {context.guild.name}",
            color=0x01f5b6
      )
      embed.set_author(
            name="Antinuke"
      )
      embed.add_field(
            name="Whitelisted Role",
            value=f"<@&{wlrole}>",
            inline=True
      )
      embed.add_field(
            name="Logging channel",
            value=f"<#{channel}>",
            inline=True
      )
      embed.add_field(
            name="Commands:",
            value="- </antinuke channel:1035065859162513408> - To change the log channel\n- </whitelist add:1035065859162513409> - To add a user to whitelist\n- </whitelist role:1035065859162513409> - To add a role to antinuke whitelist",
            inline=False
      )
      embed.set_thumbnail(
            url = "https://cdn.discordapp.com/attachments/1027593292642275418/1028516662221226024/Proton.png"
      )  
      embed.set_footer(
            text="Made with 💖 by proton Developement"
      )
      await context.send(embed=embed)


    @antinuke.command(
      name = "channel",
      description="Set the channel for antinuke logging",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(channel="The channel where you want to set antinuke logging")
    async def channel(self, context: Context, channel: discord.TextChannel) -> None:
      g = getConfig(context.guild.id)
      g['log_channel'] = channel.id
      updateConfig(context.guild.id, g)
      embed = discord.Embed(
            description=f"The log channel has been updated to {channel.mention}",
            color=0x01f5b6
      )
      await context.send(embed=embed)

    @antinuke.command(
      name = "features",
      description="shows Bots Antinuke Features",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    async def fea(self, context: Context) -> None:
      embed = discord.Embed(
            description=" Anti Ban \n Anti Unban \n Anti Kick\n Anti Channel\n Anti Role\n Anti Member Role\n Anti Guild \n Anti Webhook \n\n Type </antinuke features:1035065859162513408> To Check Features in Slash",
            color=0x01f5b6
      )
      embed.set_author(
            name="Anti Nuke"
      )
      embed.set_thumbnail(
            url = "https://cdn.discordapp.com/attachments/1027593292642275418/1028516662221226024/Proton.png"
      )
      await context.send(embed=embed)      

    @commands.hybrid_group(
        name="whitelist",
        description="shows Whitelist",
    )  
    @checks.not_blacklisted()
    @guild_owner_only()
    @commands.has_permissions(administrator=True)
    async def whitelist(self, context: Context) -> None:
      g = getConfig(context.guild.id)
      whitelisted = g['whitelist']   
      result = ' '
      for i in whitelisted:
                  user2 = self.bot.get_user(i)
                  if user2 == None:
                        user = 'Unable to Fetch Name'
                  else:
                        user = user2.mention
                  result += f"{user}: {i}\n"
      if whitelisted == []:
                  return await context.send("There are no whitelisted users in this server, do `/whitelist add` to whitelist a user of your choice!")
      else:
                    embed = discord.Embed(title=f'Whitelisted users for {context.guild.name}', description=result,
                                          color=0x01f5b6)
                    await context.send(embed=embed)
        
    
    @whitelist.command(
      name = "add",
      description="",
    )
    @checks.not_blacklisted()
    @guild_owner_only()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(user="User to be added to antinuke whitelist")
    async def wladd(self, context: Context, user: discord.User) -> None:
      g = getConfig(context.guild.id)
      whitelisted = g["whitelist"]
      me = user
      if me.id in whitelisted:
        await context.send(f"<@{me.id}> is already in whitelist")
      else:
        g["whitelist"].append(me.id)
        updateConfig(context.guild.id, g)
        embed = discord.Embed(
            description=f"{user.mention} Has Been Added To Whitelist",
            color=0x01f5b6
        )
        await context.send(embed=embed)    

    @whitelist.command(
      name = "remove",
      description="",
    )
    @checks.not_blacklisted()
    @guild_owner_only()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(user="User to be  remove from antinuke whitelist")
    async def wlr(self, context: Context, user: discord.User) -> None:
      g = getConfig(context.guild.id)
      whitelisted = g["whitelist"]
      me = user
      if me.id not in whitelisted:
        await context.send(f"<@{me.id}> is not in whitelist")
      else:
        g["whitelist"].remove(me.id)
        updateConfig(context.guild.id, g)
        embed = discord.Embed(
            description=f"{user.mention} Has Been Removed From Whitelist",
            color=0x01f5b6
        )
        await context.send(embed=embed)        

    @whitelist.command(
      name = "role",
      description="",
    )
    @checks.not_blacklisted()
    @guild_owner_only()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added to whitelist")
    async def wlrole(self, context: Context, role: discord.Role) -> None:
      g = getConfig(context.guild.id)
      g["wlrole"] = role.id
      updateConfig(context.guild.id, g)
      embed = discord.Embed(
            description=f"{role.mention} Has Been Added To Whitelist",
            color=0x01f5b6
      )
      await context.send(embed=embed)           



async def setup(bot):
    await bot.add_cog(Security(bot))