import random
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from helpers import checks
from utils.checks import getConfig, updateConfig
from typing import Optional, Union
class VcRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """VcRoles commands"""

    def help_custom(self):
		      emoji = '<:vc:1040653079915286688>'
		      label = "Vc Setup"
		      description = "Shows all Vc Commands"
		      return emoji, label, description   

    async def add_role(self, *, role: int, member: discord.Member):
        if member.guild.me.guild_permissions.manage_roles:
            role = discord.Object(id=int(role))
            await member.add_roles(role, reason="Proton | Vc Role [Joined vc]")  

    async def remove_role(self, *, role: int, member: discord.Member):
        if member.guild.me.guild_permissions.manage_roles:
            role = discord.Object(id=int(role))
            await member.remove_roles(role, reason="Proton | Vc Role [Left vc]")            

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
          if data := getConfig(member.guild.id):
            if not before.channel and after.channel:                
                for role in data.get("vcrole", []):
                  await self.add_role(role=role, member=member)
                  
            elif before.channel and not after.channel:
                for role in data.get("vcrole", []):
                  await self.remove_role(role=role, member=member)
                  


    @commands.hybrid_group(
        name="vcrole",
        description="shows vcrole commands and modules",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    async def vcrole(self, context: Context):
        ...

    @vcrole.command(
      name = "add",
      description="Add a role to vcrole",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def add(self, context: Context, role: discord.Role) -> None:
        if data := getConfig(context.guild.id):
            if len(data.get("vcrole", [])) > 10:
                embed = discord.Embed(
                        description="Vc role Has Reached Its Limit",
                        color=0x01f5b6
                ) 
                return await context.send(embed=discord.Embed)

            rta = data['vcrole']
            if role.id in rta:
              embed = discord.Embed(
                        description=f"{role.mention} is already a Vc role",
                        color=0x01f5b6
              ) 
              return await context.send(embed=discord.Embed)
            else:
              data["vcrole"].append(role.id)
              updateConfig(context.guild.id, data)
              embed = discord.Embed(
                      description=f"{role.mention} Has Been Added To Vc role",
                      color=0x01f5b6
              )
              await context.send(embed=discord.Embed) 

    @vcrole.command(
      name = "show",
      description="shows the vc role for server",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    async def show(self, context: Context) -> None:
        g = getConfig(context.guild.id)
        guild = context.guild
        vcrole = g['vcrole']  
        result = ' '
        for i in vcrole:
          role1 = guild.get_role(i)
          if role1 == None:
            role = 'Unable to Role'
          else:
            role = role1.mention       
            result += f"{role}: {i}\n"
        if vcrole == []:
                  return await context.send("There are no Vc roles in the server")
        else:
                    embed = discord.Embed(title=f'Vc Role : {context.guild.name}', description=result,
                                          color=0x01f5b6)
                    await context.send(embed=discord.Embed)  
            
          

    @vcrole.command(
      name = "remove",
      description="remove the Vc role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be removed")
    async def remove(self, context: Context, role: discord.Role) -> None:
        if data := getConfig(context.guild.id):
            rta = data['vcrole']
            if role.id not in rta:
              embed = discord.Embed(
                        description=f"{role.mention} is already not a Vc role",
                        color=0x01f5b6
              ) 
              return await context.send(embed=discord.Embed)
            else:
              data["vcrole"].remove(role.id)
              updateConfig(context.guild.id, data)
              embed = discord.Embed(
                      description=f"{role.mention} Has Been Removed From Vc role",
                      color=0x01f5b6
              )
              await context.send(embed=discord.Embed) 




    @commands.hybrid_group(description="Disconnects the member from vc")
    @commands.has_guild_permissions(move_members=True)
    async def vckick(self, ctx, *, member: discord.Member):
        if member.voice is None:
            return await ctx.reply(f"{str(member)} Is not connected in any of the voice channel")
        ch = member.voice.channel.mention
        await member.edit(voice_channel=None, reason=f"Disconnected by {str(ctx.author)}")
        return await ctx.reply(f"{str(member)} has been disconnected from {ch}")
    
    @commands.hybrid_group(description="Disconnects all the members in vc")
    @commands.has_guild_permissions(administrator=True)
    async def vckickall(self, ctx):
        if ctx.author.voice is None:
            return await ctx.reply("You are not connected in any of the voice channel")
        count=0
        ch = ctx.author.voice.channel.mention
        for member in ctx.author.voice.channel.members:
            await member.edit(voice_channel=None, reason=f"Disconnected by {str(ctx.author)}")
            count+=1
        return await ctx.reply(f"Disconnected {count} members from {ch}")

    @commands.hybrid_group(description="Mute a member in vc")
    @commands.has_guild_permissions(mute_members=True)
    async def vcmute(self, ctx, *, member: discord.Member):
        if member.voice is None:
            return await ctx.reply(f"{str(member)} Is not connected in any of the voice channel")
        if member.voice.mute == True:
            return await ctx.reply(f"{str(member)} Is already muted in the voice channel")
        ch = member.voice.channel.mention
        await member.edit(mute=True, reason=f"Muted by {str(ctx.author)}")
        return await ctx.reply(f"{str(member)} has been muted in {ch}")

    @commands.hybrid_group(description="Unmute a member in vc")
    @commands.has_guild_permissions(mute_members=True)
    async def vcunmute(self, ctx, *, member: discord.Member):
        if member.voice is None:
            return await ctx.reply(f"{str(member)} Is not connected in any of the voice channel")
        if member.voice.mute == False:
            return await ctx.reply(f"{str(member)} Is already unmuted in the voice channel")
        ch = member.voice.channel.mention
        await member.edit(mute=False, reason=f"Unmuted by {str(ctx.author)}")
        return await ctx.reply(f"{str(member)} has been unmuted in {ch}")
    
    @commands.hybrid_group(description="Mute all the members in vc")
    @commands.has_guild_permissions(administrator=True)
    async def vcmuteall(self, ctx):
        if ctx.author.voice is None:
            return await ctx.reply(f"You are not connected in any of the voice channel")
        count=0
        ch = ctx.author.voice.channel.mention
        for member in ctx.author.voice.channel.members:
            if member.voice.mute == False:
                await member.edit(mute=True, reason=f"Muted by {str(ctx.author)}")
                count+=1
        return await ctx.reply(f"Muted {count} members in {ch}")

    @commands.hybrid_group(description="Unmute all the members in vc")
    @commands.has_guild_permissions(administrator=True)
    async def vcunmuteall(self, ctx):
        if ctx.author.voice is None:
            return await ctx.reply(f"You are not connected in any of the voice channel")
        count=0
        ch = ctx.author.voice.channel.mention
        for member in ctx.author.voice.channel.members:
            if member.voice.mute == True:
                await member.edit(mute=False, reason=f"Unmuted by {str(ctx.author)}")
                count+=1
        return await ctx.reply(f"Unmuted {count} members in {ch}")

    @commands.hybrid_group(description="Deafen a member in vc")
    @commands.has_guild_permissions(deafen_members=True)
    async def vcdeaf(self, ctx, *, member: discord.Member):
        if member.voice is None:
            return await ctx.reply(f"{str(member)} Is not connected in any of the voice channel")
        if member.voice.deaf == True:
            return await ctx.reply(f"{str(member)} Is already deafen in the voice channel")
        ch = member.voice.channel.mention
        await member.edit(deafen=True, reason=f"Deafen by {str(ctx.author)}")
        return await ctx.reply(f"{str(member)} has been Deafen in {ch}")

    @commands.hybrid_group(description="Undeafen a member in vc")
    @commands.has_guild_permissions(deafen_members=True)
    async def vcundeafen(self, ctx, *, member: discord.Member):
        if member.voice is None:
            return await ctx.reply(f"{str(member)} Is not connected in any of the voice channel")
        if member.voice.deaf == False:
            return await ctx.reply(f"{str(member)} Is already undeafen in the voice channel")
        ch = member.voice.channel.mention
        await member.edit(deafen=False, reason=f"Undeafen by {str(ctx.author)}")
        return await ctx.reply(f"{str(member)} has been undeafen in {ch}")
    
    @commands.hybrid_group(description="Deafen all the members in vc")
    @commands.has_guild_permissions(administrator=True)
    async def vcdeafenall(self, ctx):
        if ctx.author.voice is None:
            return await ctx.reply(f"You are not connected in any of the voice channel")
        count=0
        ch = ctx.author.voice.channel.mention
        for member in ctx.author.voice.channel.members:
            if member.voice.deaf == False:
                await member.edit(deafen=True, reason=f"Deafen by {str(ctx.author)}")
                count+=1
        return await ctx.reply(f"Deafen {count} members in {ch}")

    @commands.hybrid_group(description="Undeafen all the members in vc")
    @commands.has_guild_permissions(administrator=True)
    async def vcundeafall(self, ctx):
        if ctx.author.voice is None:
            return await ctx.reply(f"You are not connected in any of the voice channel")
        count=0
        ch = ctx.author.voice.channel.mention
        for member in ctx.author.voice.channel.members:
            if member.voice.deaf == True:
                await member.edit(deafen=False, reason=f"Undeafen by {str(ctx.author)}")
                count+=1
        return await ctx.reply(f"Undeafen {count} members in {ch}")
    
    @commands.hybrid_group(description="Undeafen all the members in vc")
    @commands.has_guild_permissions(administrator=True)
    async def moveall(self, ctx, *, channel: discord.VoiceChannel):
        if ctx.author.voice is None:
            return await ctx.reply("You are not connected in any of the voice channel")
        try:
            ch = ctx.author.voice.channel.mention
            nch = channel.mention
            count = 0
            for member in ctx.author.voice.channel.members:
                await member.edit(voice_channel=channel, reason=f"Moved by {str(ctx.author)}")
                count+=1
            await ctx.reply(embed=discord.Embed(description=f"{count} Members Moved From {ch} to {nch}"))
        except:
            await ctx.reply(embed=discord.Embed(description="Invalid Voice channel"))















async def setup(bot):
    await bot.add_cog(VcRoles(bot))