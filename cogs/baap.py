import os
import discord
import datetime
import time
import asyncio
import aiohttp
import json
import re
from simpcalc import simpcalc
from discord.ext import commands, tasks
from discord.utils import escape_markdown
import asyncio
import validators
import json as json_but_pain
from discord import Embed
import datetime
import time
from typing import Optional, Union, List
import random

OWNERS = [985097344880082964,975012142640169020]

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
characters = "!@#$%&amp;*"
numbers = "1234567890"
email_fun = [
    '69420', '8008135', 'eatsA$$', 'PeekABoo',
    'TheShire', 'isFAT', 'Dumb_man', 'Ruthless_gamer',
    'Sexygirl69', 'Loyalboy69', 'likesButts'
]
passwords = [
    'animeislife69420', 'big_awoogas', 'red_sus_ngl',
    'IamACompleteIdiot', 'YouWontGuessThisOne',
    'yetanotherpassword', 'iamnottellingyoumypw',
    'SayHelloToMyLittleFriend', 'ImUnderYourBed',
    'TellMyWifeILoveHer', 'P@$$w0rd', 'iLike8008135', 'IKnewYouWouldHackIntoMyAccount',
    'BestPasswordEver', 'JustARandomPassword', 'VoteEpicBotUwU'
]
DMs = [
    "send nudes please", "i invited epicbot and i got a cookie",
    "i hope my mum doesn't find my nudes folder",
    "please dont bully me", "https://youtu.be/oHg5SJYRHA0",
    "i like bananas", "i use discord in light mode",
    "if you are reading this u shud vote epicbot", "send feet pics when",
    "sUbScRiBe To mY yOuTuBe ChAnNeL", "the impostor is sus", "python makes me horny"
]
discord_servers = [
    "Sons of Virgins", "Small Benis Gang", "Gamers United",
    "Anime Server 69420", "Cornhub", "Femboy Gang"
]


async def wait_for_msg(ctx: commands.Context, timeout: int, msg_to_edit: discord.Message) -> Union[discord.Message, str]:
    def c(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        msg = await ctx.bot.wait_for("message", timeout=timeout, check=c)
        try:
            await msg.delete()
        except Exception:
            pass
        if msg.content.lower() == 'cancel':
            ctx.command.reset_cooldown(ctx)
            await msg_to_edit.edit(
                content="",
                embed=discord.Embed(
                    title=f" Cancelled!",
                    color=0x01f5b6
                )
            )
            return 'pain'
    except asyncio.TimeoutError:
        ctx.command.reset_cooldown(ctx)
        await msg_to_edit.edit(
            content="",
            embed=error_embed(
                f" Too late!",
                "You didn't answer in time! Please re-run the command."
            )
        )
        return 'pain'
    return msg


class Confirm(discord.ui.View):
    def __init__(self, context: commands.Context, timeout: Optional[int] = 300, user: Optional[Union[discord.Member, discord.User]] = None):
        super().__init__(timeout=timeout)
        self.value = None
        self.context = context
        self.user = user or self.context.author

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
    async def yes(self, b, i):
        self.value = True
        self.stop()

    @discord.ui.button(label='No', style=discord.ButtonStyle.red)
    async def no(self, b, i):
        self.value = False
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("You cannot interact in other's commands.", ephemeral=True)
            return False
        return True

class Paginator(discord.ui.View):
    def __init__(self, ctx: commands.Context, embeds: List[discord.Embed]):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.embeds = embeds
        self.current = 0

    async def edit(self, msg, pos):
        em = self.embeds[pos]
        em.set_footer(text=f"Page: {pos+1}/{len(self.embeds)}")
        await msg.edit(embed=em)

    @discord.ui.button(emoji='◀️', style=discord.ButtonStyle.blurple)
    async def bac(self, b, i):
        if self.current == 0:
            return
        await self.edit(i.message, self.current - 1)
        self.current -= 1

    @discord.ui.button(emoji='⏹️', style=discord.ButtonStyle.blurple)
    async def stap(self, b, i):
        await i.message.delete()

    @discord.ui.button(emoji='▶️', style=discord.ButtonStyle.blurple)
    async def nex(self, b, i):
        if self.current + 1 == len(self.embeds):
            return
        await self.edit(i.message, self.current + 1)
        self.current += 1

    async def interaction_check(self, interaction):
        if interaction.user == self.ctx.author:
            return True
        await interaction.response.send_message("Not your command ._.", ephemeral=True)
def gen_random_string(l_: int):
    uwu = ""
    for i in range(l_ + 1):
        uwu += random.choice((letters + numbers))
    return 
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

def success_embed(title, description):
    return Embed(
        title=title,
        description=description,
        color=0x01f5b6
    )

def error_embed(title, description):
    return Embed(
        title=title,
        description=description,
        color=0x01f5b6
    )
async def process_embeds_from_json(bot, array, json, replace: bool = True):
    embed = Embed()

    if replace:
        poggers = await replace_things_in_string_fancy_lemao(bot, array, json_but_pain.dumps(json))
        uwu_json = json_but_pain.loads(poggers)
    else:
        uwu_json = json

    content = None if "plainText" not in json else uwu_json['plainText']

    embed_title = None if "title" not in json else uwu_json['title']
    embed_url = None if "url" not in json else uwu_json['url']
    embed_desc = None if "description" not in json else uwu_json['description']
    embed_image = None if "image" not in json else uwu_json['image']
    embed_thumbnail = None if "thumbnail" not in json else uwu_json['thumbnail']
    embed_color = None if "color" not in json else uwu_json['color']
    field_count = 0

    if embed_color == "0x01f5b6":
        embed_color = 0x01f5b6
    if embed_color == "0x01f5b6":
        embed_color = 0x01f5b6

    embed_author = {}
    embed_footer = {}

    if "author" in json:
        if "name" not in uwu_json['author']:
            return 'pain author name'
        embed_author.update({
            "name": uwu_json['author']['name'],
            "url": None if "url" not in uwu_json['author'] else uwu_json['author']['url'],
            "icon_url": None if "icon_url" not in uwu_json['author'] else uwu_json['author']['icon_url']
        })
    if "footer" in json:
        if "text" not in uwu_json['footer']:
            return 'pain footer text'
        embed_footer.update({
            "text": uwu_json['footer']['text'],
            "icon_url": None if "icon_url" not in uwu_json['footer'] else uwu_json['footer']['icon_url']
        })
    if "fields" in json:
        for e in uwu_json['fields']:
            if e['name'] != "" and e['value'] != "":
                embed.add_field(
                    name=e['name'],
                    value=e['value'],
                    inline=e['inline']
                )
                field_count += 1
            else:
                return 'pain empty fields'

    if embed_title is not None:
        embed.title = embed_title
    if embed_desc is not None:
        embed.description = embed_desc
    if embed_url is not None:
        embed.url = embed_url
    if embed_image is not None:
        embed.set_image(url=embed_image)
    if embed_thumbnail is not None:
        embed.set_thumbnail(url=embed_thumbnail)
    if embed_color is not None:
        embed.color = embed_color

    if len(embed_author) != 0:
        if embed_author['url'] is None and embed_author['icon_url'] is None:
            embed.set_author(name=embed_author['name'])
        elif embed_author['url'] is None and embed_author['icon_url'] is not None:
            embed.set_author(name=embed_author['name'], icon_url=embed_author['icon_url'])
        elif embed_author['url'] is not None and embed_author['icon_url'] is None:
            embed.set_author(name=embed_author['name'], url=embed_author['url'])
        else:
            embed.set_author(name=embed_author['name'], url=embed_author['url'], icon_url=embed_author['icon_url'])

    if len(embed_footer) != 0:
        if embed_footer['icon_url'] is None:
            embed.set_footer(text=embed_footer['text'])
        else:
            embed.set_footer(text=embed_footer['text'], icon_url=embed_footer['icon_url'])

    if (embed_url is not None and not validators.url(embed_url)) or (embed_image is not None and not validators.url(embed_image)) or (embed_thumbnail is not None and not validators.url(embed_thumbnail)):
        return 'pain invalid urls'
    if len(embed_author) != 0:
        if embed_author['url'] is not None and not validators.url(embed_author['url']):
            return 'pain invalid urls'
        if embed_author['icon_url'] is not None and not validators.url(embed_author['icon_url']):
            return 'pain invalid urls'
    if len(embed_footer) != 0:
        if embed_footer['icon_url'] is not None and not validators.url(embed_footer['icon_url']):
            return 'pain invalid urls'

    if embed_title is None and embed_desc is None and len(embed_author) == 0 and len(embed_footer) == 0 and field_count == 0 and embed_image is None:
        return 'pain empty embed'

    return [content, embed]
















class InteractiveView(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__(timeout=None)
        self.expr = ""
        self.calc = simpcalc.Calculate()
        self.ctx = ctx

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="1", row=0)
    async def one(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "1"
        await interaction.edit(f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="2", row=0)
    async def two(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "2"
        await interaction.edit(f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="3", row=0)
    async def three(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "3"
        await interaction.edit(f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="➕", row=0)
    async def plus(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "+"
        await interaction.edit(f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="4", row=1)
    async def last(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "4"
        await interaction.edit(f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="5", row=1)
    async def five(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "5"
        await interaction.edit(f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="6", row=1)
    async def six(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "6"
        await interaction.edit(f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="➗", row=1)
    async def divide(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "/"
        await interaction.edit(f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="7", row=2)
    async def seven(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "7"
        await interaction.edit(f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="8", row=2)
    async def eight(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "8"
        await interaction.edit(f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="9", row=2)
    async def nine(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "9"
        await interaction.edit(f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="✖️", row=2)
    async def multiply(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "*"
        await interaction.edit(f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label=".", row=3)
    async def dot(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "."
        await interaction.edit(f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="0", row=3)
    async def zero(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "0"
        await interaction.edit(f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="=", row=3)
    async def equal(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            self.expr = await self.calc.calculate(self.expr)
        except errors.BadArgument:
            return await interaction.response.send_message("Um, looks like you provided a wrong expression....")
        await interaction.edit(f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="-", row=3)
    async def minus(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "-"
        await interaction.edit(f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label="(", row=4)
    async def left_bracket(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += "("
        await interaction.edit(f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.green, label=")", row=4)
    async def right_bracket(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr += ")"
        await interaction.edit(f"```\n{self.expr}\n```")

    @discord.ui.button(style=discord.ButtonStyle.red, label="AC", row=4)
    async def clear(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.expr = ""
        await interaction.edit(f"```\n> {self.expr}\n```")


class loda(commands.Cog, description="Commands that make your Discord experience nicer!"):
    def __init__(self, bot):
        self.bot = bot

        self.regex = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")
    def help_custom(self):
       emoji = '<:c2h_heroes:1040736631591800952>'
       label = "Owner"
       description = "Shows Owner Command"
       return emoji, label, description 
      
    @property
    def session(self):
        return self.bot.http._HTTPClient__session  # type: ignore

    async def _run_code(self, *, lang: str, code: str):
        res = await self.session.post(
            "https://emkc.org/api/v1/piston/execute",
            json={"language": lang, "source": code},
        )
        return await res.json()

    ## #@commands.cooldown(1, 10, commands.BucketType.user)
    # @commands.hybrid_group(help="Set an alarm!", aliases=['setalarm'])
    # async def alarm(self, ctx: commands.Context, time_: int = None, timezone: TimeZone = None, *, text: str = None):
    #     pass

    ## #@commands.cooldown(1, 10, commands.BucketType.user)
    # @commands.hybrid_group(help="Delete an alarm!")
    # async def delalarm(self, ctx: commands.Context, id_: str):
    #     prefix = ctx.clean_prefix
    #     if id_ is None:
    #         ctx.command.reset_cooldown(ctx)
    #         return await ctx.reply(embed=error_embed(
    #             f" Invalid Usage!",
    #             f"Please enter an id.\nCorrect Usage: `{prefix}delalarm <id>`\nExample: `{prefix}delalarm s0MUcHp41N`"
    #         ))
    #     for e in self.bot.alarms:
    #         if e["_id"] == id_ and e['user_id'] == ctx.author.id:
    #             await ctx.reply(embed=success_embed(
    #                 f" Deleted!",
    #                 f"The alarm with ID: `{id_}` has been deleted."
    #             ))
    #             self.bot.alarms.pop(self.bot.alarms.index(e))
    #             await self.bot.alarms_db.delete_one({"_id": id_, "user_id": ctx.author.id})
    #             return
    #     return await ctx.reply(embed=error_embed(
    #         f" Not found!",
    #         f"The alarm with ID: `{id_}` does not exist."
    #     ))

    ## #@commands.cooldown(1, 10, commands.BucketType.user)
    # @commands.hybrid_group(help="Check your current alarms!")
    # async def alarms(self, ctx: commands.Context):
    #     prefix = ctx.clean_prefix
    #     embed = discord.Embed(
    #         title=f" Your Alarms!",
    #         color=0x01f5b6
    #     )
    #     ah_yes = self.bot.alarms
    #     pain = []
    #     for e in ah_yes:
    #         if e['user_id'] == ctx.author.id:
    #             pain.append(e)
    #     if len(pain) == 0:
    #         embed.description = f"You don't have any alarms set.\nYou can use `{prefix}alarm <time> <text>` to set an alarm."
    #     else:
    #         for aa in pain:
    #             embed.add_field(
    #                 name=f"ID: `{aa['_id']}`",
    #                 value=f"{aa['text']} - <t:{aa['time']}:t>",
    #                 inline=False
    #             )
    #         embed.set_footer(text=f"You can delete alarms using {prefix}delalarm <id>")
    #     await ctx.reply(embed=embed)

    # @commands.hybrid_group(help="Start a poll!", aliases=['startpoll', 'createpoll', 'makepoll'])
    ## #@commands.cooldown(3, 60, commands.BucketType.guild)
    # async def poll(self, ctx: commands.Context, *, question: str):
    #     pass

   # #@commands.cooldown(1, 10, commands.BucketType.user)

    @commands.hybrid_group(help="Change the bot's status")
    @commands.is_owner()
    async def changestatus(self, ctx: commands.Context, *, status: str):
        await self.bot.change_presence(
            activity=discord.Game(name=status),
            status=discord.Status.online
        )
        await ctx.message.add_reaction('👌')




    @commands.hybrid_group(aliases=['getcache'], help="Get cache!")
    @commands.is_owner()
    async def get_cache(self, ctx: commands.Context):
        msg = await ctx.reply(f" Working on it...")
        await self.bot.get_cache()
        await msg.edit(content="Done!")


    @commands.hybrid_group(aliases=['updatedb'], help="Update the database!")
    @commands.is_owner()
    async def update_db(self, ctx: commands.Context, db=None):
        if db is None:
            return await ctx.reply("""
Please select a database next time:
- prefixes
- serverconfig
            """)
        msg = await ctx.reply(f" Updating...")
        if db.lower() in ['prefixes', 'prefix']:
            await self.bot.update_prefixes_db()
        if db.lower() in ['server', 'serverconfig']:
            await self.bot.update_serverconfig_db()
        return await msg.edit(content="Updated!")

async def setup(bot):
    await bot.add_cog(loda(bot)) 