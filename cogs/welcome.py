import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from helpers import checks
from utils.checks import getConfig, updateConfig

em = "<:Arrow_12:1029600851083407420>"

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def help_custom(self):
        emoji = '<:welcome:1040652681267650580>'
        label = "Welcome"
        description = "Shows Welcome Commands"
        return emoji, label, description  

    @commands.hybrid_group(
        name="greet",
        description="shows greet commands and modules",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    async def greet(self, context: Context):
        embed = discord.Embed(title="Prton | Welcome Commands", color=0x01f5b6)
        embed.add_field(
            name="usage",
            value=
            f"{em} greet message <message>\n{em} greet channel <channel>\n{em} greet disable\n{em} greetenable\n{em} greet test",
            inline=False)
        embed.add_field(
            name="description",
            value=
            f"{em} `greet message` - Sets the welcome to a message\n{em} `greet channel` - Sets the welcome channel\n{em} `greet disable` - Disables the welcome message\n{em} `greet enable` - Enables the welcome message\n{em} `greet test` - Test the welcome message",
            inline=False)
        embed.add_field(
            name="variables",
            value=
            "<:Arrow_12:1029600851083407420> `{user.id}`\n<:Arrow_12:1029600851083407420> `{user.name}`\n<:Arrow_12:1029600851083407420> `{user.mention}`\n<:Arrow_12:1029600851083407420> `{user.tag}`\n<:Arrow_12:1029600851083407420> `{server.name}`\n<:Arrow_12:1029600851083407420> `{server.membercount}`",
            inline=False)
        await context.send(embed=embed)

    @greet.command(
      name = "message",
      description="Set the welcome message",
    )
    @commands.has_permissions(manage_channels=True)
    @checks.not_blacklisted()
    @app_commands.describe(message="Type The text which you want to be set in welcome")    
    async def message(self, context: Context, message: str) -> None:
        g = getConfig(context.guild.id)
        g['message'] = message
        updateConfig(context.guild.id, g)
        embed = discord.Embed(
            description="The Welcome message has been updated",
            color=0x01f5b6
        )
        await context.send(embed=embed)

    @greet.command(
      name = "channel",
      description="Set the channel for welcome message",
    )
    @commands.has_permissions(manage_channels=True)
    @checks.not_blacklisted()
    @app_commands.describe(channel="The channel where you want to set Welcome message")
    async def channel(self, context: Context, channel: discord.TextChannel) -> None:
      g = getConfig(context.guild.id)
      g['channel'] = channel.id
      updateConfig(context.guild.id, g)
      embed = discord.Embed(
            description=f"The Welcome channel has been updated to {channel.mention}",
            color=0x01f5b6
      )
      await context.send(embed=embed)

    @greet.command(
      name = "disable",
      description="Disable the greet module",
    )
    @commands.has_permissions(manage_channels=True)
    @checks.not_blacklisted()
    async def disable(self, context: Context) -> None:
      g = getConfig(context.guild.id)
      if g['wen'] == False:
        embed = discord.Embed(
            description=f"Greet Module Is Already Disable",
            color=0x01f5b6
        )
        await context.send(embed=embed)
      else:
        g['wen'] = False
        updateConfig(context.guild.id, g)  
        embed = discord.Embed(
            description=f"Greet Module Has Been Disabled",
            color=0x01f5b6
        )
        await context.send(embed=embed)
      
    @greet.command(
      name = "enable",
      description="Enable the greet module",
    )
    @commands.has_permissions(manage_channels=True)
    @checks.not_blacklisted()
    async def enable(self, context: Context) -> None:
      g = getConfig(context.guild.id)
      if g['wen'] == True:
        embed = discord.Embed(
            description="Greet Module Is Already Enable",
            color=0x01f5b6
        )
        await context.send(embed=embed)
      else:
        g['wen'] = True
        updateConfig(context.guild.id, g)  
        embed = discord.Embed(
            description="Greet Module Has Been Enabled",
            color=0x01f5b6
        )
        await context.send(embed=embed)

    @greet.command(
      name = "test",
      description="Test the welcome setup",
    )
    @commands.has_permissions(manage_channels=True)
    @checks.not_blacklisted()
    async def test(self, context: Context) -> None:
        g = getConfig(context.guild.id)
        if g['wen'] != True:
            embed = discord.Embed(
            description="Greet module is not enabled use `/greet enable` to enable it",
            color=0x01f5b6
            )
            return await context.send(embed=embed)
        if g["message"] == None:
            embed = discord.Embed(
            description="Greet message is not set use `/greet message` to set it",
            color=0x01f5b6
            )
            return await context.send(embed=embed)
        if g["channel"] == None:
            embed = discord.Embed(
            description="Greet channel is not set use `/greet channel` to set it",
            color=0x01f5b6
            )
            return await context.send(embed=embed)

        channel = self.bot.get_channel(g["channel"])
        message = g["message"]
        user = context.author
        if "{user.id}" in message:
            message = message.replace("{user.id}", "%s" % (user.id))

        if "{user.mention}" in message:
            message = message.replace("{user.mention}", "%s" % (user.mention))

        if "{user.tag}" in message:
            message = message.replace("{user.tag}",
                                      "%s" % (user.discriminator))

        if "{user.name}" in message:
            message = message.replace("{user.name}", "%s" % (user.name))

        if "{user.avatar}" in message:
            message = message.replace("{user.avatar}",
                                      "%s" % (user.avatar_url))

        if "{server.name}" in message:
            message = message.replace("{server.name}",
                                      "%s" % (user.guild.name))

        if "{server.membercount}" in message:
            message = message.replace("{server.membercount}",
                                      "%s" % (user.guild.member_count))

        if "{server.icon}" in message:
            message = message.replace("{server.icon}",
                                      "%s" % (user.guild.icon_url))

        try:
            await channel.send(message)
            embed = discord.Embed(
            description="Sucessfully tested welcome message",
            color=0x01f5b6
            )
            await context.send(embed=embed)
        except Exception:
            embed = discord.Embed(
            description="Error in sending message pls try later or contact our support team",
            color=0x01f5b6
            )
            await context.send(embed=embed)




async def setup(bot):
    await bot.add_cog(Welcome(bot))
