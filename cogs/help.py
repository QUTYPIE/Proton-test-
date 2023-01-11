import string
import discord
import asyncio
from discord.ext import commands
from datetime import datetime, timedelta
from views import help as vhelp #need big refactor

MAIN_COLOR = 0x01f5b6

class HelpCommand(commands.HelpCommand):
    """Help command"""

    async def on_help_command_error(self, ctx, error) -> None:
        handledErrors = [
            commands.CommandOnCooldown, 
            commands.CommandNotFound
        ]

        if not type(error) in handledErrors:
            print("! Help command Error :", error, type(error), type(error).__name__)
            return await super().on_help_command_error(ctx, error)

    def command_not_found(self, string) -> None:
        raise commands.CommandNotFound(f"Command {string} is not found")

    async def send_bot_help(self, mapping) -> None:
        allowed = 5
        close_in = round(datetime.timestamp(datetime.now() + timedelta(minutes=allowed)))
        embed = discord.Embed(title = "Help", description=f"<:Reply_Black:1041435008054870118> Prefix for this server `:` **`-`** or **`/`**\n<:Reply_Black:1041435008054870118> Total commands **`:`** {len(set(self.context.bot.walk_commands()))}\n<:Reply_Black:1041435008054870118> Type `-help <command | module>` for more info", color = MAIN_COLOR).set_thumbnail(url = "https://cdn.discordapp.com/attachments/1027593292642275418/1028516662221226024/Proton.png").set_image(url="https://media2.giphy.com/media/GHKlVpc6ThFB9Zk41M/giphy_s.gif").set_footer(text="Made with 💖 by Proton Development")
        embed.add_field(name="**Basic Modules**", value="<:invisible:1041438272280346675><:General_Info:1041435128896962560> **`:`** General\n<:invisible:1041438272280346675><:astroz_mod:1041446848356950056> **`:`** Moderation\n<:invisible:1041438272280346675><:astroz_music:1041435202951585815> **`:`** Music\n<:invisible:1041438272280346675><:astroz_fun:1041435254256324689> **`:`** Fun\n<:invisible:1041438272280346675><:text:1041435291916963901> **`:`** Text\n<:invisible:1041438272280346675><:NYISGCoOwner:1041435742238408757> **`:`** Owner\n<:invisible:1041438272280346675><:ApplicationDidntRespond:1041438213883035789> **`:`** Autoresponder\n<:invisible:1041438272280346675><:Games:1041439557897425006> **`:`** Games", inline=True) 
        embed.add_field(name="**Server Modules**", value="""<:invisible:1041438272280346675><a:Welcome:1030058947345916024> **`:`** Welcome\n<:invisible:1041438272280346675><:riverse_autorole:1041435388620853318> **`:`** Autorole\n<:invisible:1041438272280346675><:automod:1042177853925621942> **`:`** Automod\n<:invisible:1041438272280346675><a:IconServerSecurity:1041435553087901757> **`:`** Server Roles\n<:invisible:1041438272280346675><:Ticket:1041435598285705318> **`:`** Ticket\n<:invisible:1041438272280346675><:vc:1041435650731286660> **`:`** Vc Role\n<:invisible:1041438272280346675><:black_gun:1041435859410505748> **`:`** Combat\n<:invisible:1041438272280346675><:canal_nsfw:1041442232638640229> **`:`** Nsfw\n""", inline=True)  






        view = vhelp.View(mapping = mapping, ctx = self.context, homeembed = embed, ui = 2)
        message = await self.context.send(embed = embed, view = view)
        try:
            await asyncio.sleep(60*allowed)
            view.stop()
            await message.delete()
        except: pass




  
    async def send_command_help(self, command):
        cog = command.cog
        if "help_custom" in dir(cog):
            emoji, label, _ = cog.help_custom()
            embed = discord.Embed(title = f" Help · {label} : {command.name}", description=f"**Command** : {command.name}\n{command.help}", url="https://discord.gg/A4PpGEG9gB", color = MAIN_COLOR)
            params = ""
            for param in command.clean_params: 
                params += f" <{param}>"
          #  embed.add_field(name="Usage", value=f"{command.name}{params}", inline=False)
            embed.add_field(name="Aliases", value=f"{command.aliases}`")
            embed.set_footer(text="Remind : Hooks such as <> must not be used when executing commands.", icon_url=self.context.message.author.display_avatar.url)
            await self.context.send(embed=embed)

    async def send_cog_help(self, cog):
        if "help_custom" in dir(cog):
            emoji, label, _ = cog.help_custom()
            embed = discord.Embed(title = " Help ", url="https://discord.gg/A4PpGEG9gB", color = MAIN_COLOR)
            for command in cog.get_commands():
                params = ""
                for param in command.clean_params: 
                    params += f" <{param}>"
                embed.add_field(name=f"<:grl_arrow:1041438543005892699>{command.name}{params}", value=f"<:invisible:1041438272280346675><a:arrows:1041438324730101932>`{command.help}`\n", inline=False)
            embed.set_footer(text="Made By Proton Developement", icon_url=self.context.message.author.display_avatar.url)
            await self.context.send(embed=embed)

    async def send_group_help(self, group):
        prefix = self.context.clean_prefix
        embed = discord.Embed(
            title=f"Group command help: `{group.qualified_name}`",
            description=group.description,
            color=MAIN_COLOR
        ).set_author(name=self.context.bot.user.name, icon_url=self.context.bot.user.avatar.url
        ).set_footer(text=f"Requested by: {self.context.author}", icon_url=self.context.author.display_avatar.url)

        embed.add_field(
            name="Subcommands:",
            value=" | ".join([f"`{prefix}{cmd.qualified_name}{' ' + cmd.signature if cmd.signature else ''}` - {cmd.help}" for cmd in group.commands]),
            inline=False
        )
        return await self.context.send(embed=embed)
      
     

class Help(commands.Cog, name="help"):
    """Help commands."""
    def __init__(self, bot):
        self._original_help_command = bot.help_command

        attributes = {
            'name': "help",
            'aliases': ['h', '?'],
            'cooldown': commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.user) # discordpy2.0
        } 

        bot.help_command = HelpCommand(command_attrs=attributes)
        bot.help_command.cog = self
        
    def cog_unload(self):
        self.bot.help_command = self._original_help_command



async def setup(bot):
	await bot.add_cog(Help(bot))