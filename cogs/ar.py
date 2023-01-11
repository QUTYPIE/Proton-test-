import discord
from discord import app_commands
from discord.ext import commands
import json
from discord.ext.commands import Context
from helpers import checks, db_manager
import asyncio, datetime, json




class ar(commands.Cog, name="Ar"):
    def __init__(self, bot):
        self.bot = bot

    def help_custom(self):
        emoji = '<:Chatbot:1040656507957686352>'
        label = "Autoresponder"
        description = "Shows Ar Commands"
        return emoji, label, description    



    @commands.hybrid_group(description='count all autoresponses of server')
    @commands.cooldown(1, 5, commands.BucketType.user)
    @app_commands.describe(user="Shows Autoresponder Commands ")
    @commands.has_permissions(administrator=True)
    async def arshow(self, ctx):
        """
        Shows Autoresponders In Server
        """
        with open("autoresponse.json", "r") as f:
            autoresponse = json.load(f)
        autoresponsenames = []
        guild = ctx.guild
        if str(ctx.guild.id) in autoresponse:
            for autoresponsecount in autoresponse[str(ctx.guild.id)]:
              autoresponsenames.append(autoresponsecount)
            embed = discord.Embed(color=0x01f5b6)
            st, count = "", 1
            for autoresponse in autoresponsenames:
                    st += f"`{'0' + str(count) if count < 10 else count}. `    **{autoresponse.upper()}**\n"
                    test = count
                    count += 1
              
                    embed.title = f"Autoresponders Counts In {guild} -> (`{test}`)"
        embed.description = st
        embed.set_thumbnail(url = "https://images-ext-1.discordapp.net/external/tMdg89dAyTk8I-58lEANKBW_SQJ7_I4gzvTb9AhS-CY/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1027428088562319391/9cf546646fcd8b81a108fd7b24c3e732.png")
        await ctx.send(embed=embed) 




  
    @commands.hybrid_group(aliases=["create"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    @app_commands.describe(user="Create Autoresponder Commands ")
    @commands.has_permissions(administrator=True)
    async def arcreate(self, ctx, name , *, message):
        """
        Creates Ar Of The Server
        """
        with open("autoresponse.json", "r") as f:
            autoresponse = json.load(f)
        numbers = []
        if str(ctx.guild.id) in autoresponse:
            for autoresponsecount in autoresponse[str(ctx.guild.id)]:
              numbers.append(autoresponsecount)
            if len(numbers) >= 10:
                return await ctx.send(embed=discord.Embed(title=f'You can\'t add more than 10 autoresponses in a server', color=0x01f5b6))
        if str(ctx.guild.id) in autoresponse:
            if name in autoresponse[str(ctx.guild.id)]:
                return await ctx.send(embed=discord.Embed(title=f' The autoresponse `{name}` is already in the server', color=0x01f5b6))
        if str(ctx.guild.id) in autoresponse:
            autoresponse[str(ctx.guild.id)][name] = message
            with open("autoresponse.json", "w") as f:
              json.dump(autoresponse, f, indent=4)
            return await ctx.reply(embed=discord.Embed(title=f'Successfully Created Ar : `{name}` ', color=0x01f5b6))

        data = {
            name : message,
        }
        autoresponse[str(ctx.guild.id)] = data

        with open("autoresponse.json", "w") as f:
            json.dump(autoresponse, f, indent=4)
            return await ctx.reply(embed=discord.Embed(title=f' Successfully Created Ar : `{name}`', color=0x01f5b6))


          
    @commands.hybrid_group(aliases=["delete"])
    @commands.cooldown(1, 5, commands.BucketType.user)   
    @app_commands.describe(user="Delete Autoresponder Commands ")
    @commands.has_permissions(administrator=True)
    async def ardelete(self, ctx, name):
        """
        Deletes Ar Of The Server
        """
        with open("autoresponse.json", "r") as f:
            autoresponse = json.load(f)
            
        if str(ctx.guild.id) in autoresponse:
            if name in autoresponse[str(ctx.guild.id)]:
                del autoresponse[str(ctx.guild.id)][name]
                with open("autoresponse.json", "w") as f:
                    json.dump(autoresponse, f, indent=4)
                return await ctx.reply(embed=discord.Embed(title=f'Successfully Removed Ar : `{name}`', color=0x01f5b6))
            else:
                return await ctx.reply(embed=discord.Embed(title=f'No autoresponse found with the name `{name}`', color=0x01f5b6))
        else:
            return await ctx.reply(embed=discord.Embed(title=f'There is no autoresponses in the server', color=0x01f5b6))
  
    @commands.hybrid_group(aliases=["edit"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @app_commands.describe(user="Edit Autoresponder Commands ")
    @commands.has_permissions(administrator=True)
    async def aredit(self, ctx, name , *, message):
        """
        Edits Ar Of The Server
        """
        with open("autoresponse.json", "r") as f:
            autoresponse = json.load(f)
        if str(ctx.guild.id) in autoresponse:
            if name in autoresponse[str(ctx.guild.id)]:
                autoresponse[str(ctx.guild.id)][name] = message
                with open("autoresponse.json", "w") as f:
                    json.dump(autoresponse, f, indent=4)
                return await ctx.send(embed=discord.Embed(title=f'Successfully Edited Ar : `{name}`', color=0x01f5b6))
        else:
            return await ctx.send(embed=discord.Embed(title=f'No Ar Found In {ctx.guild}', color=0x01f5b6))



    @commands.Cog.listener() 
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.bot.user:
                return
        try:
            if message is not None:
                with open("autoresponse.json", "r") as f:
                    autoresponse = json.load(f)
                if str(message.guild.id) in autoresponse:
                    ans = autoresponse[str(message.guild.id)][message.content.lower()]
                    return await message.channel.send(ans)
        except:
            pass

async def setup(bot):
    await bot.add_cog(ar(bot))