import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from helpers import checks
from utils.checks import getConfig, updateConfig




class Autorole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
      
    def help_custom(self):
        emoji = '<:riverse_autorole:1040652756769321050>'
        label = "Autorole"
        description = "Shows Autorole Comamnds"
        return emoji, label, description   
    
   

    async def add_role(self, *, role: int, member: discord.Member):
        if member.guild.me.guild_permissions.manage_roles:
            role = discord.Object(id=int(role))
            if not member._roles.has(role):
                await member.add_roles(role, reason="Proton | Auto Role")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if data := getConfig(member.guild.id):
            for role in data.get("autorole", []):
                await self.add_role(role=role, member=member)

            if member.bot:
                for role in data.get("bots", []):
                    await self.add_role(role=role, member=member)
            else:
                for role in data.get("humans", []):
                    await self.add_role(role=role, member=member)

# Schema: {"guild": INT, "bots": LIST, "humans": LIST, "autorole": []}


    @commands.hybrid_group(
      description="Set the autorole for humans",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def addhumans(self, context: Context, role: discord.Role) -> None:
        if data := getConfig(context.guild.id):
            if len(data.get("humans", [])) > 10:
                embed = discord.Embed(
                        description="Autorole Humans Has Reached Its Limit",
                        color=0x01f5b6
                ) 
                return await context.send(embed=embed)

            rta = data['humans']
            if role.id in rta:
              embed = discord.Embed(
                        description=f"{role.mention} is already a autorole",
                        color=0x01f5b6
              ) 
              return await context.send(embed=embed)
            else:
              data["humans"].append(role.id)
              updateConfig(context.guild.id, data)
              embed = discord.Embed(
                      description=f"{role.mention} Has Been Added To Autorole Humans",
                      color=0x01f5b6
              )
              await context.send(embed=embed) 
              
    @commands.hybrid_group(
      description="Set the autorole for everyone",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def atadd(self, context: Context, role: discord.Role) -> None:
        if data := getConfig(context.guild.id):
            if len(data.get("autorole", [])) > 10:
                embed = discord.Embed(
                        description="Autorole Humans Has Reached Its Limit",
                        color=0x01f5b6
                ) 
                return await context.send(embed=embed)

            rta = data['autorole']
            if role.id in rta:
              embed = discord.Embed(
                        description=f"{role.mention} is already a autorole",
                        color=0x01f5b6
              ) 
              return await context.send(embed=embed)
            else:
              data["autorole"].append(role.id)
              updateConfig(context.guild.id, data)
              embed = discord.Embed(
                      description=f"{role.mention} Has Been Added To Autorole",
                      color=0x01f5b6
              )
              await context.send(embed=embed) 

    @commands.hybrid_group(
      name = "bots",
      description="Set the autorole for bots",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def bots(self, context: Context, role: discord.Role) -> None:
        if data := getConfig(context.guild.id):
            if len(data.get("bots", [])) > 10:
                embed = discord.Embed(
                        description="Autorole Humans Has Reached Its Limit",
                        color=0x01f5b6
                ) 
                return await context.send(embed=embed)

            rta = data['bots']
            if role.id in rta:
              embed = discord.Embed(
                        description=f"{role.mention} is already a autorole",
                        color=0x01f5b6
              ) 
              return await context.send(embed=embed)
            else:
              data["bots"].append(role.id)
              updateConfig(context.guild.id, data)
              embed = discord.Embed(
                      description=f"{role.mention} Has Been Added To Autorole Bots",
                      color=0x01f5b6
              )
              await context.send(embed=embed) 
  
    @commands.hybrid_group(
      description="remove the autorole for everyone",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be removed")
    async def atremove(self, context: Context, role: discord.Role) -> None:
        if data := getConfig(context.guild.id):
            rta = data['autorole']
            if role.id not in rta:
              embed = discord.Embed(
                        description=f"{role.mention} is already not a autorole",
                        color=0x01f5b6
              ) 
              return await context.send(embed=embed)
            else:
              data["autorole"].remove(role.id)
              updateConfig(context.guild.id, data)
              embed = discord.Embed(
                      description=f"{role.mention} Has Been Removed From Autorole",
                      color=0x01f5b6
              )
              await context.send(embed=embed) 

    @commands.hybrid_group(
      name = "removehumans",
      description="remove the autorole for humans",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be removed")
    async def removeh(self, context: Context, role: discord.Role) -> None:
        if data := getConfig(context.guild.id):
            rta = data['humans']
            if role.id not in rta:
              embed = discord.Embed(
                        description=f"{role.mention} is already not a autorole",
                        color=0x01f5b6
              ) 
              return await context.send(embed=embed)
            else:
              data["humans"].remove(role.id)
              updateConfig(context.guild.id, data)
              embed = discord.Embed(
                      description=f"{role.mention} Has Been Removed From Autorole Humans",
                      color=0x01f5b6
              )
              await context.send(embed=embed) 
  
    @commands.hybrid_group(
      name = "removebots",
      description="remove the autorole for bots",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be removed")
    async def removeb(self, context: Context, role: discord.Role) -> None:
        if data := getConfig(context.guild.id):
            rta = data['bots']
            if role.id not in rta:
              embed = discord.Embed(
                        description=f"{role.mention} is already not a autorole",
                        color=0x01f5b6
              ) 
              return await context.send(embed=embed)
            else:
              data["bots"].remove(role.id)
              updateConfig(context.guild.id, data)
              embed = discord.Embed(
                      description=f"{role.mention} Has Been Removed From Autorole Bots",
                      color=0x01f5b6
              )
              await context.send(embed=embed) 

async def setup(bot):
    await bot.add_cog(Autorole(bot))