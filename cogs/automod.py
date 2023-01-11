import discord
from discord.ext import commands
import json
import datetime
import httpx

cd = commands.CooldownMapping.from_cooldown(6, 7, commands.BucketType.user)
headers = {'Authorization': 'MTAyNzQyODA4ODU2MjMxOTM5MQ.GKPGmx.L3D8YzPm5QZXa_DciY-76yYQ5WZvFh8eNl2pv0'}




class auto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def help_custom(self):
        emoji = '<:automod:1042177853925621942>'
        label = "Automod"
        description = "Shows Automod Commands"
        return emoji, label, description    

    @commands.Cog.listener()
    async def antispamm_event(self, message):
      with open("automod.json", "r") as f:
        idk = json.load(f)
      bucket = cd.get_bucket(message)
      retry = bucket.update_rate_limit()
      if retry:
        if str(message.guild.id) not in idk or idk[str(message.guild.id)] == "off":
          return
        elif str(message.guild.id) in idk and idk[str(message.guild.id)]== "on":
          if message.author.guild_permissions.manage_messages:
              return
          else:
            if message.author.id != self.bot.user.id:
              duration = datetime.timedelta(minutes=20)
              await message.author.timeout_for(duration, reason="Spamming")
              await message.channel.send(embed=discord.Embed(color=discord.Colour(0x01f5b6), title="Automod Detection", description=f'{message.author.mention} Has Been Muted For Spamming'))

    @commands.Cog.listener()
    async def antilinks_event(self, message):
      duration = datetime.timedelta(minutes=5)
      with open("automod.json", "r") as f:
        conf = json.load(f)
      if str(message.guild.id) not in conf or conf[str(message.guild.id)] == "disable":
        return
      elif str(message.guild.id) in conf and conf[str(message.guild.id)] == "enable":
        if message.author.guild_permissions.manage_messages:
          return
        else:
          if "https://discord.gg/" in message.content:
        
  
            httpx.delete(f"https://discord.com/api/v9/channels/{message.channel.id}/messages/{message.id}", headers=headers)
            await message.author.timeout_for(duration, reason="Sending server invite")
            await message.channel.send(embed=discord.Embed(title="Automod Antilink", description=f'<:codez_tick:1041780005400743987> | Successfully Muted {message.author.mention} For Posting Links '))
            return
          if "discord.gg" in message.content:
                    httpx.delete(f"https://discord.com/api/v9/channels/{message.channel.id}/messages/{message.id}", headers=headers)
          await message.author.timeout_for(duration, reason="Sending server invite")
          await message.channel.send(embed=discord.Embed(title="Automod Antilink", description=f'<:codez_tick:1041780005400743987> | Successfully Muted {message.author.mention} For Posting Links '))
          if "https://" in message.content:
                    httpx.delete(f"https://discord.com/api/v9/channels/{message.channel.id}/messages/{message.id}", headers=headers)
          await message.author.timeout_for(duration, reason="Sending links")
          await message.channel.send(embed=discord.Embed(title="Automod Antilink", description=f'<:codez_tick:1041780005400743987> | Successfully Muted {message.author.mention} For Posting Links '))
          if ".gg/" in message.content:
                    httpx.delete(f"https://discord.com/api/v9/channels/{message.channel.id}/messages/{message.id}", headers=headers)
          await message.author.timeout_for(duration, reason="Sending server invite")
          await message.channel.send(embed=discord.Embed(title="Automod Antilink", description=f'<:codez_tick:1041780005400743987> | Successfully Muted {message.author.mention} For Posting Links '))


          
          if "http://" in message.content:
  
  
  
                    httpx.delete(f"https://discord.com/api/v9/channels/{message.channel.id}/messages/{message.id}", headers=headers)
          await message.author.timeout_for(duration, reason="Sending links")
          await message.channel.send(embed=discord.Embed(title="Automod Antilink", description=f'<:codez_tick:1041780005400743987> | Successfully Muted {message.author.mention} For Posting Links '))
          if "Discord.gg" in message.content:
            httpx.delete(f"https://discord.com/api/v9/channels/{message.channel.id}/messages/{message.id}", headers=headers)
            await message.author.timeout_for(duration, reason="Sending server invite")
            await message.channel.send(embed=discord.Embed(title="Automod Antilink", description=f'<:codez_tick:1041780005400743987> | Successfully Muted {message.author.mention} For Posting Links '))
            if "discord.com/invite" in message.content:
                    httpx.delete(f"https://discord.com/api/v9/channels/{message.channel.id}/messages/{message.id}", headers=headers)
            await message.author.timeout_for(duration, reason="Posting Links Here")
            await message.channel.send(embed=discord.Embed(title="Automod Antilink", description=f'<:codez_tick:1041780005400743987> | Successfully Muted {message.author.mention} For Posting Links '))
        
    @commands.group()
    async def automod(self, ctx):
      """Automod Toggles For Server"""
      ...



    @automod.command(description="Stops User For Spamming")
    @commands.has_permissions(administrator=True)
    async def antispam(self, ctx, toggle):
      with open("automod.json", "r") as f:
        idk = json.load(f)
      if toggle == "on":
          idk[str(ctx.guild.id)] = "on"
          await ctx.reply(embed=discord.Embed(color=discord.Colour(0x01f5b6), title="Automod Antispam", description="<:codez_tick:1041780005400743987> | Successfully Enabled Antispam"))
      elif toggle == "off":
          idk[str(ctx.guild.id)] = "off"
          await ctx.reply(embed=discord.Embed(color=discord.Colour(0x01f5b6), title="Automod Antispam", description="<:codez_tick:1041780005400743987> | Successfully Disabled Antispam"))
      else:
          await ctx.reply(embed=discord.Embed(color=discord.Colour(0x01f5b6), title="Automod Error!!", description="Command Is Invalid \n Usage = `on / off`"))
      with open('automod.json', 'w') as f:
        json.dump(idk, f, indent=4)


    @automod.command(description="Stops User For Sending Links")
    @commands.has_permissions(administrator=True)
    async def antilink(self, ctx, toggle):
      with open("automod.json", "r") as f:
        idk = json.load(f)
      if toggle == "on":
          idk[str(ctx.guild.id)] = "on"
          await ctx.reply(embed=discord.Embed(color=discord.Colour(0x01f5b6), title="Automod Antilink", description="<:codez_tick:1041780005400743987> | Successfully Enabled Antilink"))
      elif toggle == "off":
          idk[str(ctx.guild.id)] = "off"
          await ctx.reply(embed=discord.Embed(color=discord.Colour(0x01f5b6), title="Automod Antispam", description="<:codez_tick:1041780005400743987> | Successfully Enabled Antilink"))
      else:
        await ctx.reply(embed=discord.Embed(color=discord.Colour(0x01f5b6), title="Automod Error!!", description="Command Is Invalid \n Usage = `on / off`"))
      with open('antisp', 'w') as f:
        json.dump(idk, f, indent=4)



async def setup(bot):
    await bot.add_cog(auto(bot))