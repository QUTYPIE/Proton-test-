import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from helpers import checks, db_manager
import asyncio, datetime, json, re
from discord.ext.commands import Converter
from discord.ext import commands
from io import BytesIO
from discord.ext import commands
from typing import Union, Optional
from discord.utils import escape_markdown
from typing import List, Optional, Union
import time
from afks import afks
from discord.utils import get
from discord.utils import get
import discord
import psutil


def convert(time):
    time_dict = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 3600 * 24,
        'w': 3600 * 24 * 7,
        'y': 3600 * 24 * 365
    }

    unit = time[-1]

    if unit not in time_dict:
        return -1
    try:
        value = int(time[:-1])
    except Exception:
        return -2
    if value <= 0:
        return -3

    if unit == 's':
        real_unit = 'second(s)'
    if unit == 'm':
        real_unit = 'minute(s)'
    if unit == 'h':
        real_unit = 'hour(s)'
    if unit == 'd':
        real_unit = 'day(s)'
    if unit == 'w':
        real_unit = 'week(s)'
    if unit == 'y':
        real_unit = 'year(s)'

    return [value * time_dict[unit], value, real_unit]

def remove(afk):
    if "[AFK]" in afk.split():
        return " ".join(afk.split()[1:])
    else:
        return afk
class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout: Optional[int] = None):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"This is {self.ctx.author.mention}'s command, not yours.", ephemeral=True)
            return False
        return True

class UserinfoView(BasicView):

    def __init__(self, ctx: commands.Context, timeout: Optional[int] = None, embeds: List[discord.Embed] = None):
        super().__init__(ctx, timeout=timeout)
        self.embeds = embeds or []

class Lower(Converter):
    async def convert(self, ctx: Context, argument: str):
        return argument.lower()

class Paginator(discord.ui.View):
    def __init__(self, ctx: commands.Context, embeds:discord.Embed):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.embeds = embeds
        self.current = 0

    async def edit(self, msg, pos):
        em = self.embeds[pos]
        em.set_footer(text=f"Page : {pos+1}/{len(self.embeds)}")
        await msg.edit(embed=em)

class PaginatorText(discord.ui.View):
    def __init__(self, ctx: commands.Context, stuff: str):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.stuff = stuff
        self.current = 0

    async def edit(self, msg, pos):
        await msg.edit(content=self.stuff[pos])



      
class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot):
        self.bot = bot
        self.tasks = []
    def help_custom(self):
        emoji = '<:moderation:1040651841270198292>'
        label = "Moderation"
        description = "Shows Moderater Commands"
        return emoji, label, description    
  

    @commands.hybrid_group(
        name="kick",
        description="Kick a user out of the server.",
    )
    @commands.has_permissions(kick_members=True)
    @checks.not_blacklisted()
    @app_commands.describe(user="The user that should be kicked.", reason="The reason why the user should be kicked.")
    async def kick(self, context: Context, user: discord.User, *, reason: str = "Not specified") -> None:
        """
        Kick a user out of the server.
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
        if context.guild.me.top_role <= member.top_role:
            embed = discord.Embed(
                title="Error!",
                description="User role is equal or above your role",
                color=0x01f5b6
            )
            await context.send(embed=embed)
        else:
            try:
                embed = discord.Embed(
                    title="User Kicked!",
                    description=f"**{member}** was kicked by **{context.author}**!",
                    color=0x01f5b6
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await context.send(embed=embed)
                try:
                    await member.send(
                        f"You were kicked by **{context.author.name} in {context.guild.name}**!\nReason: {reason}"
                    )
                except:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.kick(reason=reason)
            except:
                embed = discord.Embed(
                    title="Error!",
                    description="An error occurred while trying to kick the user. Make sure my role is above the role of the user you want to kick.",
                    color=0x01f5b6
                )
                await context.send(embed=embed)



  
    @commands.hybrid_group(
        name="nick",
        description="Change the nickname of a user on a server.",
    )
    @commands.has_permissions(manage_nicknames=True)
    @checks.not_blacklisted()
    @app_commands.describe(user="The user that should have a new nickname.", nickname="The new nickname that should be set.")
    async def nick(self, context: Context, user: discord.User, *, nickname: str = None) -> None:
        """
        Change the nickname of a user on a server.
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                title="Changed Nickname!",
                description=f"**{member}'s** new nickname is **{nickname}**!",
                color=0x01f5b6
            )
            await context.send(embed=embed)
        except:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to change the nickname of the user. Make sure my role is above the role of the user you want to change the nickname.",
                color=0x01f5b6
            )
            await context.send(embed=embed)


  
    @commands.hybrid_group(
        name="ban",
        description="Bans a user from the server.",
    )
    @commands.has_permissions(ban_members=True)
    @checks.not_blacklisted()
    @app_commands.describe(user="The user that should be banned.", reason="The reason why the user should be banned.")
    async def ban(self, context: Context, user: discord.User, *, reason: str = "Not specified") -> None:
        """
        Bans a user from the server.
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
        try:
            if context.guild.me.top_role <= member.top_role:
              embed = discord.Embed(
                title="Error!",
                description="User role is equal or above your role",
                color=0x01f5b6
              )
              await context.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="User Banned!",
                    description=f"**{member}** was banned by **{context.author}**!",
                    color=0x01f5b6
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await context.send(embed=embed)
                try:
                    await member.send(f"You were banned by **{context.author}**!\nReason: {reason}")
                except:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.ban(reason=reason)
        except:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. Make sure my role is above the role of the user you want to ban.",
                color=0x01f5b6
            )
            await context.send(embed=embed)

    @commands.hybrid_group(
        name="warning",
        description="Manage warnings of a user on a server.",
    )
    @commands.has_permissions(manage_messages=True)
    @checks.not_blacklisted()
    async def warning(self, context: Context) -> None:
        """
        Manage warnings of a user on a server.
        """
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                title="Error!",
                description="Please specify a subcommand.\n\n**Subcommands:**\n`add` - Add a warning to a user.\n`remove` - Remove a warning from a user.\n`list` - List all warnings of a user.",
                color=0x01f5b6
            )
            await context.send(embed=embed)

    @warning.command(
        name="add",
        description="Adds a warning to a user in the server.",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(user="The user that should be warned.", reason="The reason why the user should be warned.")
    async def warning_add(self, context: Context, user: discord.User, *, reason: str = "Not specified") -> None:
        """
        Warns a user in his private messages.
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
        total = db_manager.add_warn(
            user.id, context.guild.id, context.author.id, reason)
        embed = discord.Embed(
            title="User Warned!",
            description=f"**{member}** was warned by **{context.author}**!\nTotal warns for this user: {total}",
            color=0x01f5b6
        )
        embed.add_field(
            name="Reason:",
            value=reason
        )
        await context.send(embed=embed)
        try:
            await member.send(f"You were warned by **{context.author}**!\nReason: {reason}")
        except:
            # Couldn't send a message in the private messages of the user
            await context.send(f"{member.mention}, you were warned by **{context.author}**!\nReason: {reason}")

    @warning.command(
        name="remove",
        description="Removes a warning from a user in the server.",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(user="The user that should get their warning removed.", warn_id="The ID of the warning that should be removed.")
    async def warning_remove(self, context: Context, user: discord.User, warn_id: int) -> None:
        """
        Warns a user in his private messages.
        """
        member = context.guild.get_member(user.id) or await context.guild.fetch_member(user.id)
        total = db_manager.remove_warn(warn_id, user.id, context.guild.id)
        embed = discord.Embed(
            title="User Warn Removed!",
            description=f"I've removed the warning **#{warn_id}** from **{member}**!\nTotal warns for this user: {total}",
            color=0x01f5b6
        )
        await context.send(embed=embed)

    @warning.command(
        name="list",
        description="Shows the warnings of a user in the server.",
    )
    @commands.has_guild_permissions(manage_messages=True)
    @checks.not_blacklisted()
    @app_commands.describe(user="The user you want to get the warnings of.")
    async def warning_list(self, context: Context, user: discord.User):
        """
        Shows the warnings of a user in the server.
        """
        warnings_list = db_manager.get_warnings(user.id, context.guild.id)
        embed = discord.Embed(
            title=f"Warnings of {user}",
            color=0x01f5b6
        )
        description = ""
        if len(warnings_list) == 0:
            description = "This user has no warnings."
        else:
            for warning in warnings_list:
                description += f"• Warned by <@{warning[2]}>: **{warning[3]}** (<t:{warning[4]}>) - Warn ID #{warning[5]}\n"
        embed.description = description
        await context.send(embed=embed)




    @commands.hybrid_group(aliases=['tb'])
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tempban(self, ctx, member: discord.Member, time, d, *, reason="No Reason"):
      if member == None:
        embed = discord.Embed(f"{ctx.message.author}, Please enter a valid user!")
        await ctx.send(embed=embed)
      else:
        guild = ctx.guild
        embed = discord.Embed(description=f" {member.mention} has been banned Successfully", colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Reason: ", value=reason, inline=False)
        embed.add_field(name="Time left for the ban:", value=f"{time}{d}", inline=False)
        await ctx.send(embed=embed)
        await guild.ban(user=member)
        
        if d == "s":
          await asyncio.sleep(int(time))
          await guild.unban(user=member)
          if d == "m":
            await asyncio.sleep(int(time*60))
            await guild.unban(user=member)
            if d == "h":
              await asyncio.sleep(int(time*60*60))
              await guild.unban(user=member)
              if d == "d":
                await asyncio.sleep(time*60*60*24)
                await guild.unban(int(user=member))

         
    @commands.hybrid_group(
        name="hackban",
        description="Bans a user without the user having to be in the server.",
    )
    @commands.has_permissions(ban_members=True)
    @checks.not_blacklisted()
    @app_commands.describe(user_id="The user ID that should be banned.", reason="The reason why the user should be banned.")
    async def hackban(self, context: Context, user_id: str, *, reason: str = "Not specified") -> None:
        """
        Bans a user without the user having to be in the server.
        """
        try:
            await self.bot.http.ban(user_id, context.guild.id, reason=reason)
            user = self.bot.get_user(int(user_id)) or await self.bot.fetch_user(int(user_id))
            embed = discord.Embed(
                title="User Banned!",
                description=f"**{user} (ID: {user_id}) ** was banned by **{context.author}**!",
                color=0x01f5b6
            )
            embed.add_field(
                name="Reason:",
                value=reason
            )
            await context.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. Make sure ID is an existing ID that belongs to a user.",
                color=0x01f5b6
            )
            await context.send(embed=embed)



    @commands.hybrid_group()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"This channel's slowmode has been set to {seconds}")

    @commands.hybrid_group()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
      channel = channel or ctx.channel
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      overwrite.send_messages = False
      await channel.set_permissions(ctx.guild.default_role,
                                  overwrite=overwrite,
                                  reason=f"Channel Locked By {ctx.author}")
      await ctx.reply(f"Succefully Locked {channel.mention}", mention_author=False)


    @commands.hybrid_group(
        name='avatar',
        aliases=['av', 'ac', 'ah', 'pfp', 'avi', 'ico', 'icon'],
        help='get any discord user profile picture'
    )
    async def avatar(self, ctx, user: discord.Member = None):
        button2 = discord.ui.Button(label='Avatar', style=discord.ButtonStyle.blurple)
        button = discord.ui.Button(label='Banner', style=discord.ButtonStyle.danger)
        button3 = discord.ui.Button(label='Server Av', style=discord.ButtonStyle.success)
        try:
          if user == None:
             user = ctx.author
          else:  
             user = await self.bot.fetch_user(user.id)
        except AttributeError:
            user = ctx.author
        webp = user.avatar.replace(format='webp')
        jpg = user.avatar.replace(format='jpg')
        png = user.avatar.replace(format='png')
        view = discord.ui.View()
        view.add_item(button2)
        view.add_item(button)
        view.add_item(button3)
        async def button2_callback(interaction: discord.Interaction):
          embed1 = discord.Embed(
            color=000000,
            title=f"{user}'s Avatar",description=f"[[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp})]"
            if not user.avatar.is_animated()
            else f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp}) | [`GIF`]({user.avatar.replace(format='gif')})")
          embed1.set_image(url=user.avatar.url)
          embed1.set_footer(text=f"Requested by {ctx.author}")
          await interaction.response.send_message(embed=embed1, ephemeral=True)

          
        async def button_callback(interaction: discord.Interaction):
          embed5=discord.Embed(color = 000000, title=f"{user}'s Banner").set_footer(text=f"Requested by {ctx.author}")
          bannerUser = await self.bot.fetch_user(user.id)
          if not bannerUser.banner:
             await interaction.response.send_message('User has no banner', ephemeral=True)   
          embed5.set_image(url=bannerUser.banner) 
          await interaction.response.send_message(embed=embed5, ephemeral=True)

        async def button3_callback(interaction: discord.Interaction):
          serverav = discord.Embed(color=00000,title=f"{user} Server Avatar")
          serverav.set_image(url=user.display_avatar.url)
          await interaction.response.send_message(embed=serverav, ephemeral=True)


      
        avemb = discord.Embed(
            color=000000,
            title="About User's Profile", url="https://discord.gg/A4PpGEG9gB", description="*Use Buttons Below To Check User's Avatar and Banner*").set_thumbnail(url =ctx.author.avatar.url).set_footer(text="Server Av is visible to author")
        button2.callback = button2_callback
        button.callback = button_callback
        button3.callback = button3_callback
        await ctx.send(embed=avemb, mention_author=True, view=view)

      
    @commands.hybrid_group()
    async def servericon(self, ctx):
        button2 = discord.ui.Button(label='Server Avatar', style=discord.ButtonStyle.blurple)
        button = discord.ui.Button(label='Server Banner', style=discord.ButtonStyle.danger)
        view = discord.ui.View()
        view.add_item(button2)
        view.add_item(button)
        server = ctx.guild
        webp = server.icon.replace(format='webp')
        jpg = server.icon.replace(format='jpg')
        png = server.icon.replace(format='png')
        async def button2_callback(interaction: discord.Interaction):
          embed1 = discord.Embed(
            color=000000,
            title=f"{server}'s Icon",description=f"[[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp})]"
            if not server.icon.is_animated()
            else f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp}) | [`GIF`]]({server.icon.replace(format='gif')})"
        )
          embed1.set_image(url=server.icon.url)
          embed1.set_footer(text=f"Requested by {ctx.author}")
          await interaction.response.send_message(embed=embed1, ephemeral=True)
        async def button_callback(interaction: discord.Interaction):
          if not ctx.guild.banner:
             await interaction.response.send_message('This server does not have any banner!')
          embed5=discord.Embed(title=f'{ctx.guild.name}\'s Banner', color = 000000)
          embed5.set_image(url=ctx.guild.banner)
          await interaction.response.send_message(embed=embed5, ephemeral=True)

        avemb = discord.Embed(
            color=000000,
            title="About Server Profile info", url="https://discord.gg/A4PpGEG9gB", description="*Use Buttons Below To See Server Avatar and Banner*").set_thumbnail(url =ctx.author.avatar.url)
        button2.callback = button2_callback
        button.callback = button_callback
        await ctx.send(embed=avemb, view=view)

      
    @commands.hybrid_group(aliases=['unl'])
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
      channel = channel or ctx.channel
      overwrite = channel.overwrites_for(ctx.guild.default_role)
      overwrite.send_messages = True
      await channel.set_permissions(ctx.guild.default_role,
                                  overwrite=overwrite,
                                  reason=f"Channel Unlocked By {ctx.author}")
      await ctx.reply(f"Succefully Unlocked {channel.mention}", mention_author=False)


    @commands.hybrid_group(aliases=[("inv")])
    async def invite(self, ctx):
        button2 = discord.ui.Button(label='Invite', emoji="💎",  style=discord.ButtonStyle.blurple)
        button1 = discord.ui.Button(label='Server', emoji="🔱",  style=discord.ButtonStyle.success)
        button = discord.ui.Button(label='Back', emoji="↩️",  style=discord.ButtonStyle.danger)
        view = discord.ui.View()
        view.add_item(button2)
        view.add_item(button1)
        view.add_item(button)
        async def button2_callback(interaction: discord.Interaction):
          embed1 = discord.Embed(description=f'[Click To Invite Me](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot%20applications.commands)', color=00000)
          await interaction.response.send_message(embed=embed1, ephemeral=True)
        async def button_callback(interaction: discord.Interaction):
          embed5=discord.Embed(description="Use Buttons To Invite or Join Support Server")
          await interaction.response.send_message(embed=embed5, ephemeral=True)
        async def button1_callback(interaction: discord.Interaction):
          embed3=discord.Embed(description="**Click **[here](https://discord.gg/A4PpGEG9gB) **To Join Support Server**")
          await interaction.response.send_message(embed=embed3, ephemeral=True)
        embed=discord.Embed(description="Use Buttons To Invite or Join Support Server")
        button2.callback = button2_callback
        button1.callback = button1_callback
        button.callback = button_callback
        await ctx.send(embed=embed, view=view)


    @commands.hybrid_group(aliases=[("si")])
    async def serverinfo(self, ctx: commands.Context, *, guild_name = None):
        button2 = discord.ui.Button(label='Roles', style=discord.ButtonStyle.primary)
        button = discord.ui.Button(label='Channels', style=discord.ButtonStyle.success)
        button3 = discord.ui.Button(label='Back', style=discord.ButtonStyle.danger)
        view = discord.ui.View()
        view.add_item(button2)
        view.add_item(button)
        view.add_item(button3)
        guild = None
        if guild_name == None:
            guild = ctx.guild
        else:
            for g in self.bot.guilds:
                if g.name.lower() == guild_name.lower():
                    guild = g
                    break
                if str(g.id) == str(guild_name):
                    guild = g
                    break
        if guild == None:
            await ctx.send("I couldn't find that guild...")
            return
        findbots = sum(1 for member in ctx.guild.members if member.bot)
        a = r = 0
        m = len(guild._members)
        for member in guild.members:
            if member.guild_permissions.administrator:
                a += 1
            else:
                r += len(member.roles) > 1
        server_embed = discord.Embed(
            title="Server Information",
            description=f"**Description:** {guild.description}",
            color=00000
        )
        if guild.icon is not None:
            server_embed.set_thumbnail(url=guild.icon.url)
        chandesc = "{:,} text, {:,} voice".format(len(guild.text_channels), len(guild.voice_channels))
        online_members = 0
        bot_member     = 0
        bot_online     = 0
        nsfw_level = ''
        if ctx.guild.nsfw_level.name == 'default':
          nsfw_level = '**Default**'
        if ctx.guild.nsfw_level.name == 'explicit':
          nsfw_level = '**Explicit**'
        if ctx.guild.nsfw_level.name == 'safe':
          nsfw_level = '**Safe**'
        if ctx.guild.nsfw_level.name == 'age_restricted':
          nsfw_level = '**Age Restricted**'
        async def button2_callback(interaction: discord.Interaction):
          roles = ""
          for i in ctx.guild.roles:
            roles += "" + str(i.mention) + " | "
          embed1 = discord.Embed(title=f'{ctx.guild.name}', description=f'{roles}', color=00000)
          await interaction.response.send_message(embed=embed1, ephemeral=True)
        async def button_callback(interaction: discord.Interaction):
          channels = ""
          for i in ctx.guild.channels:
            channels += "" + str(i.mention) + " | "
          embed4 = discord.Embed(title=f'{ctx.guild.name}', description=f'{channels}', color=00000)
          await interaction.response.send_message(embed=embed4, ephemeral=True)
        async def button3_callback(interaction: discord.Interaction):
          embed8 = discord.Embed(title=f'{ctx.guild.name}', description=f"""
**Owner:** <@{guild.owner_id}>
**Created At**: <t:{int(ctx.guild.created_at.timestamp())}:D>
**System Channel:** {"None" if guild.system_channel is None else guild.system_channel.mention}
**Default Role:** {guild.default_role}
**Max Talk Bitrate: **<t:{int(ctx.guild.bitrate_limit)}:D>kbps
**Afk Channel:** {guild.afk_channel}
**NSFW level:** {nsfw_level}
**Channels:** `{chandesc}`
**Considered Large:** {guild.large}
**Verification Level:** {str(guild.verification_level).title()}
**Boost Tier:** {ctx.guild.premium_tier}
**Max Talk Bitrate: ** {int(ctx.guild.bitrate_limit)}kbps
**Boost count:** {ctx.guild.premium_subscription_count}
**Boost Role:** {guild.premium_subscriber_role.mention}
**Nitro Level:** {guild.premium_tier}
**Shard Id:** {guild.shard_id+1} / {self.bot.shard_count}
**Join Position: ** {position}/{total}
**Population Rank:** {position}/{total}
**Emoji count:** Total - {c} | EmoInfo - {emojiinfo}
**Memberinfo:** Admins: {a} | Other roles: {r} | No roles: {m - a - r}
**Threads:** {len(guild.threads)}
**Total Bots:** {findbots}
**Administrators:** {len([i for i in ctx.guild.members if i.guild_permissions.administrator])}
"""
            , color=00000)
          embed8.set_footer(text=f"Requested by {ctx.author}")
          embed8.add_field(name="Custom Emoji", value=len(guild.emojis))
          embed8.add_field(
            name="**__Count Info__** :",
            value=f"""
**Members: ** `{len(guild.members)}` | `{user_string}`
**Humans:** `{len(list(filter(lambda m: not m.bot, guild.members)))}`
**Bots:** `{len(list(filter(lambda m: m.bot, guild.members)))}`
            """,
            inline=True
        )
          embed8.add_field(
            name="**__Other Info__** :",
            value=f"""
**Roles:** `{len(guild.roles)}`
**Emojis:** `{len(guild.emojis)}`
**Stickers:** `{len(guild.stickers)}`
                """
        ) 
          if guild.icon is not None:
            embed8.set_thumbnail(url=guild.icon.url)
          if guild.features:
            embed8.add_field(
                name="Guild Activities :",
                value=' :  <:codez_tick:1041780005400743987>\n '.join([feature.replace('_', ' ').title() for feature in guild.features]).upper(),
                inline=False
            )
          if guild.banner is not None:
              embed8.set_image(url=guild.banner.url)
          await interaction.response.send_message(embed=embed8, ephemeral=True)
        joinedList = []
        popList    = []
        for g in self.bot.guilds:
            joinedList.append({ 'ID' : g.id, 'Joined' : g.me.joined_at })
            popList.append({ 'ID' : g.id, 'Population' : len(g.members) })
        
        joinedList = sorted(joinedList, key=lambda x:x["Joined"].timestamp() if x["Joined"] != None else -1)
        popList = sorted(popList, key=lambda x:x['Population'], reverse=True)
        
        check_item = { "ID" : guild.id, "Joined" : guild.me.joined_at }
        total = len(joinedList)
        position = joinedList.index(check_item) + 1
        for member in guild.members:
            if member.bot:
                bot_member += 1
                if not member.status == discord.Status.offline:
                        bot_online += 1
                continue
            if not member.status == discord.Status.offline:
                online_members += 1
        user_string = "{:,}/{:,} online ({:,g}%)".format(
                online_members,
                len(guild.members) - bot_member,
                round((online_members/(len(guild.members) - bot_member) * 100), 2)
        )
        b_string = "bot" if bot_member == 1 else "bots"
        user_string += "\n{:,}/{:,} {} online ({:,g}%)".format(
                bot_online,
                bot_member,
                b_string,
                round((bot_online/bot_member)*100, 2)
        )
        check_item = { "ID" : guild.id, "Population" : len(guild.members) }
        total = len(popList)
        position = popList.index(check_item) + 1
        c = len(guild.emojis)
        a = sum(getattr(e, "animated", False) for e in g.emojis)
        emojiinfo = f"Animated: {a}\nRegular: {c - a}"
        server_embed.add_field(
            name="**__Basic Info__** :",
            value=f"""
**Owner:** <@{guild.owner_id}>
**Created At**: <t:{int(ctx.guild.created_at.timestamp())}:D>
**System Channel:** {"None" if guild.system_channel is None else guild.system_channel.mention}
**Default Role:** {guild.default_role}
**Max Talk Bitrate: **<t:{int(ctx.guild.bitrate_limit)}:D>kbps
**Afk Channel:** {guild.afk_channel}
**NSFW level:** {nsfw_level}
**Channels:** `{chandesc}`
**Considered Large:** {guild.large}
**Verification Level:** {str(guild.verification_level).title()}
**Boost Tier:** {ctx.guild.premium_tier}
**Max Talk Bitrate: ** {int(ctx.guild.bitrate_limit)}kbps
**Boost count:** {ctx.guild.premium_subscription_count}
**Boost Role:** {guild.premium_subscriber_role.mention}
**Nitro Level:** {guild.premium_tier}
**Shard Id:** {guild.shard_id+1} / {self.bot.shard_count}
**Join Position: ** {position}/{total}
**Population Rank:** {position}/{total}
**Emoji count:** Total - {c} | EmoInfo - {emojiinfo}
**Memberinfo:** Admins: {a} | Other roles: {r} | No roles: {m - a - r}
**Threads:** {len(guild.threads)}
**Total Bots:** {findbots}
**Administrators:** {len([i for i in ctx.guild.members if i.guild_permissions.administrator])}
            """,
            inline=False
        )
        server_embed.add_field(name="Custom Emoji", value=len(guild.emojis))
        server_embed.add_field(
            name="**__Count Info__** :",
            value=f"""
**Members: ** `{len(guild.members)}` | `{user_string}`
**Humans:** `{len(list(filter(lambda m: not m.bot, guild.members)))}`
**Bots:** `{len(list(filter(lambda m: m.bot, guild.members)))}`
            """,
            inline=True
        )
        server_embed.add_field(
            name="**__Other Info__** :",
            value=f"""
**Roles:** `{len(guild.roles)}/250`
**Emojis:** `{len(guild.emojis)}/200`
**Stickers:** `{len(guild.stickers)}/100`
                """
        )
        if guild.features:
            server_embed.add_field(
                name="Guild Activities :",
                value=' :  <:codez_tick:1041780005400743987>\n '.join([feature.replace('_', ' ').title() for feature in guild.features]).upper(),
                inline=False
            )
        if guild.banner is not None:
            server_embed.set_image(url=guild.banner.url)
            server_embed.set_footer(text=f"Requested by {ctx.author}")
        button2.callback = button2_callback
        button.callback = button_callback
        button3.callback = button3_callback
        return await ctx.reply(embed=server_embed, view=view)


    @commands.hybrid_group(name="roleall", description="Gives a role to all members", usage="roleall <role>", aliases=["role-all", "rall"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def role_all(self, ctx, *, role: discord.Role):
        if ctx.guild.id in self.tasks:
            return await ctx.send(embed=discord.Embed(title="roleall", description="There is a roleall task already running, please wait for it to finish", color=self.color))
        await ctx.reply(embed=discord.Embed(description="Giving Role To All Users"))
        await ctx.message.add_reaction("<:codez_tick:1041780005400743987>")
        num = 0
        failed = 0
        for user in list(ctx.guild.members):
            try:
                await user.add_roles(role)
                num += 1
            except Exception:
                failed += 1
        await ctx.send(embed=discord.Embed(title="roleall", description="Successfully added **`%s`** to **`%s`** users, failed to add it to **`%s`** users" % (role.name, num, failed), color=self.color))


    @commands.hybrid_group(name="membercount",
                      description="Shows member stats",
                      usage="membercount",
                      aliases=["mc"])
    async def membercount(self, ctx):
        button2 = discord.ui.Button(label='Online', style=discord.ButtonStyle.blurple)
        button = discord.ui.Button(label='Idle', style=discord.ButtonStyle.success)
        button5 = discord.ui.Button(label='Do Not Disturb', style=discord.ButtonStyle.danger)
        button6 = discord.ui.Button(label='Offline', style=discord.ButtonStyle.grey)
        view = discord.ui.View()
        view.add_item(button2)
        view.add_item(button)
        view.add_item(button5)
        view.add_item(button6)
        online = 0
        offline = 0
        dnd = 0
        idle = 0
        bots = 0
        for member in ctx.guild.members:
            if member.status == discord.Status.online:
                online += 1
            if member.status == discord.Status.offline:
                offline += 1
            if member.status == discord.Status.dnd:
                dnd += 1
            if member.status == discord.Status.idle:
                idle += 1
            if member.bot:
                bots += 1
        async def button2_callback(interaction: discord.Interaction):
          embed1 = discord.Embed(title=f'{ctx.guild.name}', description=f"```yaml\nOnline :: {online}```").set_thumbnail(url=ctx.author.avatar.url)
          await interaction.response.send_message(embed=embed1, ephemeral=True)
          
        async def button_callback(interaction: discord.Interaction):
          embed8 = discord.Embed(title=f'{ctx.guild.name}', description=f"```adoc\nIdle :: {idle}```").set_thumbnail(url=ctx.author.avatar.url)
          await interaction.response.send_message(embed=embed8, ephemeral=True)
          
        async def button5_callback(interaction: discord.Interaction):
          embed7 = discord.Embed(title=f'{ctx.guild.name}', description=f"```yaml\nDo Not Disturb :: {dnd}```").set_thumbnail(url=ctx.author.avatar.url)
          await interaction.response.send_message(embed=embed7, ephemeral=True)

        async def button6_callback(interaction: discord.Interaction):
          embed6 = discord.Embed(title=f'{ctx.guild.name}', description=f"```yaml\nOffline :: {offline}```").set_thumbnail(url=ctx.author.avatar.url)
          await interaction.response.send_message(embed=embed6, ephemeral=True)
        embed = discord.Embed(
            title=ctx.guild.name,
            color=0x01f5b6, description=f"```yaml\nTotal Bots :: {bots}\nTotal Users :: {len(ctx.guild.members)}```")
        embed.set_thumbnail(url=ctx.guild.icon.url).set_footer(text="Made with 💖 By Proton Developement")
        button2.callback = button2_callback
        button.callback = button_callback
        button5.callback = button5_callback
        button6.callback = button6_callback
        await ctx.send(embed=embed, view=view)
      

    @commands.hybrid_group()
    @commands.guild_only()
    @commands.max_concurrency(1, per=commands.BucketType.guild)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx,amount:int=10):
        if amount >1000:
            return await ctx.send("Purge limit exceeded. Please provide an integer which is less than or equal to 1000.")
        deleted = await ctx.channel.purge(limit=amount+1)
        return await ctx.send(embed=discord.Embed(title="Proton | Mod", description=f"**Successfully Purged {len(deleted)-1} Messages**", color=0x01f5b6))
      

    async def do_removal(self, ctx, limit, predicate, *, before=None, after=None, message=True):
        if limit > 2000:
            return await ctx.send(f"Too many messages to search given ({limit}/2000)")

        if not before:
            before = ctx.message
        else:
            before = discord.Object(id=before)

        if after:
            after = discord.Object(id=after)

        try:
            deleted = await ctx.channel.purge(limit=limit, before=before, after=after, check=predicate)
        except discord.Forbidden:
            return await ctx.send("I do not have permissions to delete messages.")
        except discord.HTTPException as e:
            return await ctx.send(f"Error: {e} (try a smaller search?)")

        deleted = len(deleted)
        if message is True:
            await ctx.send(f"🚮 Successfully removed {deleted} message{'' if deleted == 1 else 's'}.")

    @purge.command()
    async def embeds(self, ctx, search=100):
        """Removes messages that have embeds in them."""
        await self.do_removal(ctx, search, lambda e: len(e.embeds))

    @purge.command()
    async def files(self, ctx, search=100):
        """Removes messages that have attachments in them."""
        await self.do_removal(ctx, search, lambda e: len(e.attachments))

    @purge.command()
    async def mentions(self, ctx, search=100):
        """Removes messages that have mentions in them."""
        await self.do_removal(ctx, search, lambda e: len(e.mentions) or len(e.role_mentions))

    @purge.command()
    async def images(self, ctx, search=100):
        """Removes messages that have embeds or attachments."""
        await self.do_removal(ctx, search, lambda e: len(e.embeds) or len(e.attachments))

    @purge.command(name="all")
    async def _remove_all(self, ctx, search=100):
        """Removes all messages."""
        await self.do_removal(ctx, search, lambda e: True)



    @purge.command(name="bots")
    async def _bots(self, ctx, search=100, prefix=None):
        """Removes a bot user's messages and messages with their optional prefix."""

        getprefix = "-"

        def predicate(m):
            return (m.webhook_id is None and m.author.bot) or m.content.startswith(tuple(getprefix))

        await self.do_removal(ctx, search, predicate)


    @purge.command(name="emojis")
    async def _emojis(self, ctx, search=100):
        """Removes all messages containing custom emoji."""
        custom_emoji = re.compile(r"<a?:(.*?):(\d{17,21})>|[\u263a-\U0001f645]")

        def predicate(m):
            return custom_emoji.search(m.content)

        await self.do_removal(ctx, search, predicate)

    @purge.command(name="reactions")
    async def _reactions(self, ctx, search=100):
        """Removes all reactions from messages that have them."""

        if search > 2000:
            return await ctx.send(f"Too many messages to search for ({search}/2000)")

        total_reactions = 0
        async for message in ctx.history(limit=search, before=ctx.message):
            if len(message.reactions):
                total_reactions += sum(r.count for r in message.reactions)
                await message.clear_reactions()

        await ctx.send(f"Successfully removed {total_reactions} reactions.")

    @purge.command(help="Clears the messages of the given user",usage="purge <user>")
    @commands.has_guild_permissions(manage_messages=True)
    async def user(self, ctx, user: discord.Member, amount: int = 10):
        if amount >1000:
            return await ctx.author.send(embed=discord.Embed(description="Purge limit Reached"))
        global counter
        counter = 0

        def check(m):
            global counter
            if counter >= amount:
                return False

            if m.author.id == user.id:
                counter += 1
                return True
            else:
                return False
        deleted = await ctx.channel.purge(limit=100, check=check)
        return await ctx.send(embed=discord.Embed(description=f"Successfully Purged User  {len(deleted)}/{amount} Messages"))

    @commands.hybrid_group(description="Shows boosters member")
    async def boosters(self, ctx):
      guild = ctx.guild
      embed = discord.Embed(title=f"{guild.name} Total Boosters \n Total No. :- `{len(guild.premium_subscribers)}`", color=0x01f5b6, description="")
      embed.set_thumbnail(url=ctx.guild.icon.url)
      for no, member in enumerate(guild.premium_subscribers, start=1):
        embed.description += f"Username :- {member} \n Mentions :- {member.mention} \n Boost Time :- <t:{round(member.premium_since.timestamp())}:R>\n\n"
      await ctx.send(embed=embed)

      
    @commands.hybrid_command(help="Search for emojis!", aliases=['searchemoji', 'findemoji', 'emojifind'])
    async def emojisearch(self, ctx: commands.Context, name: Lower = None):
        if not name:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=discord.Embed(description="Please enter a emoji!\n\nExample: `emojisearch cat`"))
        emojis = [str(emoji) for emoji in self.bot.emojis if name in emoji.name.lower() and emoji.is_usable()]
        if len(emojis) == 0:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=discord.Embed(description=f"Couldn't find any results for `{name}`, please try again."))
        paginator = commands.Paginator(prefix="", suffix="", max_size=500)
        for emoji in emojis:
            paginator.add_line(emoji)
        await ctx.reply(embed=discord.Embed(description=f"Found `{len(emojis)}` emojis"))
        if len(paginator.pages) == 1:
            return await ctx.send(paginator.pages[0])
        view = PaginatorText(ctx, paginator.pages)
        await ctx.send(paginator.pages[0], view=view)


    @commands.hybrid_command(help="Search for stickers!", aliases=['searchsticker', 'findsticker', 'stickerfind'])
    async def stickersearch(self, ctx: commands.Context, name: Lower = None):
        if not name:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=discord.Embed(description="Please enter a sticker`"))
        stickers = [sticker for sticker in self.bot.stickers if name in sticker.name.lower()]
        if len(stickers) == 0:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=discord.Embed(description=f"Couldn't find any results for `{name}` | Try Again"))
        embeds = []
        for sticker in stickers:
            embeds.append(discord.Embed(
                title=sticker.name,
                description=sticker.description,
                color=0x01f5b6,
                url=sticker.url
            ).set_image(url=sticker.url))
        await ctx.reply(embed=discord.Embed(description=f"Found `{len(embeds)}` stickers."))
        if len(embeds) == 1:
            return await ctx.send(embed=embeds[0])
        view = Paginator(ctx, embeds)
        return await ctx.send(embed=embeds[0], view=view)



 
    @commands.hybrid_group(help="Get info about a role.", aliases=[("ri")])
    async def roleinfo(self, ctx: commands.Context, role: discord.Role = None):
        prefix = ctx.clean_prefix
        if role is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=discord.Embed(description=
                f"Please mention a role to get info about.\nCorrect Usage: `roleinfo @role`"))
        embed = discord.Embed(
            title=f" Role Information",
            color=role.color
        )
        embed.add_field(
            name="Basic Info:",
            value=f"""
```adoc\n
Role Name :: {role.name}
Role ID :: {role.id}
Role Position :: {role.position}
Role Color :: {str(role.color)[1:]}
Hoisted :: {role.hoist}
Inrole Members :: {len(role.members)}
```
            """,
            inline=False
        )
        something = ""
        for permission in role.permissions:
            a, b = permission
            a = ' '.join(a.split('_')).title()
            hmm = '+' if b else '-'
            something += hmm + ' ' + a + ' | '
        embed.add_field(
            name="Role Perms :",
            value=f"```diff\n{something}\n```",
            inline=False
        )
        await ctx.reply(embed=embed)

          




    @commands.hybrid_group(help="Check bot's ping.")
    async def ping(self, ctx):
        button = discord.ui.Button(label='API', style=discord.ButtonStyle.primary)
        button2 = discord.ui.Button(label='Ping', style=discord.ButtonStyle.success)
        button3 = discord.ui.Button(label='Database', style=discord.ButtonStyle.danger)
        button4 = discord.ui.Button(label='Shards', style=discord.ButtonStyle.grey)
        view = discord.ui.View()
        view.add_item(button)
        view.add_item(button2)
        view.add_item(button3)
        view.add_item(button4)
        time1 = time.perf_counter()
        msg = await ctx.message.reply(embed=discord.Embed(title="Pinging...", color=0x01f5b6))
        time2 = time.perf_counter()

        db_time1 = time.perf_counter()

        db_time2 = time.perf_counter()

        shard_text = ""
        for shard, latency in self.bot.latencies:
            shard_text += f"Shard {shard}" + ' ' * (3 - len(str(shard))) + f': {round(latency*1000)}ms\n'
        async def button_callback(interaction: discord.Interaction):
          embed5=discord.Embed(color = 000000, title="Bot's API", description=f"{round(self.bot.latency*1000)}ms").set_footer(text=f"Requested by {ctx.author}")
          await interaction.response.send_message(embed=embed5, ephemeral=True)
        async def button2_callback(interaction: discord.Interaction):
          embed1=discord.Embed(color = 000000, title="Bot's Ping", description=f"{round((time2-time1)*1000)}ms").set_footer(text=f"Requested by {ctx.author}")
          await interaction.response.send_message(embed=embed1, ephemeral=True)
        async def button3_callback(interaction: discord.Interaction):
          embed8=discord.Embed(color = 000000, title="Bot's Database", description=f"{round((db_time2-db_time1)*1000)}ms").set_footer(text=f"Requested by {ctx.author}")
          await interaction.response.send_message(embed=embed8, ephemeral=True)
        async def button4_callback(interaction: discord.Interaction):
          embed8=discord.Embed(color = 000000, title="Bot's Shards", description=f"{shard_text}ms").set_footer(text=f"Requested by {ctx.author}")
          await interaction.response.send_message(embed=embed8, ephemeral=True)


          
        embed = discord.Embed(title=
            "Bot Latency Info", description=
            f"""
***Click Below The Button To Check Bot Ping***""", color=0x01f5b6
        ).set_thumbnail(url=self.bot.user.display_avatar.url)
        button.callback = button_callback
        button2.callback = button2_callback
        button3.callback = button3_callback
        button4.callback = button4_callback
        await msg.edit(embed=embed, view=view)


  # #@commands.cooldown(1, 10, commands.BucketType.user)
    @commands.hybrid_group(help="Get info about stickers in a message!", aliases=['stickers', 'stickerinfo'])
    async def sticker(self, ctx: commands.Context):
        ref = ctx.message.reference
        if not ref:
            stickers = ctx.message.stickers
        else:
            msg = await ctx.fetch_message(ref.message_id)
            stickers = msg.stickers
        if len(stickers) == 0:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=discord.Embed(
                f" No Stickers!",
                "There are no stickers in this message."
            ))
        embeds = []
        for sticker in stickers:
            sticker = await sticker.fetch()
            embed = discord.Embed(
                title=f" Sticker Info",
                description=f"""
**Name:** {sticker.name}
**ID:** {sticker.id}
**Description:** {sticker.description}
**URL:** [Link]({sticker.url})
{"**Related Emoji:** "+":"+sticker.emoji+":" if isinstance(sticker, discord.GuildSticker) else "**Tags:** "+', '.join(sticker.tags)}
                """,
                color=0x01f5b6
            ).set_thumbnail(url=sticker.url)
            if isinstance(sticker, discord.GuildSticker):
                embed.add_field(
                    name="Guild ID:",
                    value=f"{sticker.guild_id}",
                    inline=False
                )
            else:
                pack = await sticker.pack()
                embed.add_field(
                    name="Pack Info:",
                    value=f"""
**Name:** {pack.name}
**ID:** {pack.id}
**Stickers:** {len(pack.stickers)}
**Description:** {pack.description}
                    """,
                    inline=False
                )
                embed.set_image(url=pack.banner.url)
            embeds.append(embed)

        if len(embeds) == 1:
            await ctx.reply(embed=embeds[0])
        else:
            view = Paginator(ctx, embeds)
            await ctx.reply(embed=embeds[0], view=view)



    @commands.hybrid_command(name="rolecall", aliases=["rc"])
    @commands.guild_only()
    @commands.has_guild_permissions(move_members=True)
    @commands.bot_has_guild_permissions(move_members=True)
    async def norm_rolecall(self, ctx, role: discord.Role, voicechannel: Optional[Union[discord.VoiceChannel, discord.StageChannel]], exclusions: commands.Greedy[Union[discord.Role, discord.VoiceChannel]] = None):
      if voicechannel.permissions_for(ctx.author).view_channel is not True:
        return await ctx.send(embed=discord.Embed(title="Trying to connect to a channel you can't view 🤔", description="Im going to have to stop you right there", color=0x01f5b6))
      if voicechannel.permissions_for(ctx.author).connect is not True:
        return await ctx.send(embed=discord.Embed(title=f"You don't have permission to connect to `{voicechannel}` so I can't complete this command", color=0x01f5b6))

      moved = 0
      for member in role.members:
        if (exclusions is None or (isinstance(exclusions, list) and exclusions is not None and member not in exclusions)) and member not in voicechannel.members:
          try:
            await member.move_to(voicechannel, reason=f"Role call command by {ctx.author}")
            moved += 1
          except BaseException:
            pass

      return await ctx.send(embed=discord.Embed(title=f"Moved {moved} members with the role `{role}` to `{voicechannel}`"))













      
async def setup(bot):
    await bot.add_cog(Moderation(bot))