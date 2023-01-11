from core.bot import Bot
import asyncio
import os
import sqlite3
import traceback
from contextlib import closing
import exceptions
import discord
import json
import random
import jishaku
from discord.ext import commands
from discord.ext.commands import Context
import ast
import inspect
from lib2to3.pgen2 import token
import re
from click import command
import discord
from discord.ext import commands
import os


bot = Bot()





async def load_cogs() -> None:  
        await bot.load_extension("jishaku")
        for file in os.listdir(f"./cogs"):
          if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                tb = traceback.format_exception(type(e), e, e.__traceback__)
                tbe = "".join(tb) + ""
                print(tbe)

def init_db():
    with closing(connect_db()) as db:
        with open("database/schema.sql", "r") as f:
            db.cursor().executescript(f.read())
        db.commit()

def source(o):
    s = inspect.getsource(o).split("\n")
    indent = len(s[0]) - len(s[0].lstrip())
    return "\n".join(i[indent:] for i in s)


source_ = source(discord.gateway.DiscordWebSocket.identify)
patched = re.sub(
    r'([\'"]\$browser[\'"]:\s?[\'"]).+([\'"])', 
    r"\1Discord Android\2",  
    source_
)

loc = {}
exec(compile(ast.parse(patched), "<string>", "exec"), discord.gateway.__dict__, loc)

discord.gateway.DiscordWebSocket.identify = loc["identify"]
def connect_db():
    return sqlite3.connect("database/database.db")


bot.db = connect_db()


@bot.event
async def on_message(message: discord.Message) -> None:

    if message.author == bot.user or message.author.bot:
        return
    if message.content.lower() in [f'<@{bot.user.id}>', f'<@!{bot.user.id}>']:  
      embed = discord.Embed(
                        description="My prefix is `-`",
                        color=0x2F3136
      ) 
      await message.channel.send(embed=embed)
    await bot.process_commands(message)



@bot.command(aliases=[("ui")])
async def userinfo(ctx, *, user: discord.Member = None): # b'\xfc'
    user = ctx.author if not user else user
    if user == None:
      user = ctx.author
    async def button_callback(interaction: discord.Interaction):
      badges = ""
      if ctx.author.public_flags.hypesquad:
        badges = "Hypesquad"
      elif ctx.author.public_flags.hypesquad_balance:
        badges = "Hypesquad Balance"
      elif ctx.author.public_flags.hypesquad_bravery:
        badges = "Hypesquad Bravery"
      elif ctx.author.public_flags.hypesquad_brilliance:
        badges = "Hypesquad Brilliance"
      elif ctx.author.public_flags.early_supporter:
        badges = "Early Supporter"
      elif ctx.author.public_flags.verified_bot_developer:
        badges = "Verified Bot Developer"
      elif ctx.author.public_flags.partner:
        badges = "Partner"
      elif ctx.author.public_flags.bug_hunter:
        badges = "Bug Hunter"
      for i in badges:
        embed1 = discord.Embed(title='Badges', color = 000000)
        embed1.set_author(name=f'{user}', icon_url=f'{user.avatar}')
        await interaction.response.send_message(embed=embed1, ephemeral=True)
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=0x01f5b6)
    embed.add_field(name="User Mention", value=f"{user.mention}")
    embed.add_field(name="User Status", value=f"{user.status}")
    embed.add_field(name="Discriminator", value=f"{user.discriminator}")
    embed.add_field(name="User Roles", value=f"{len(user.roles)}")
    embed.add_field(name="Top Role", value=f"{user.top_role.mention}")
    embed.add_field(name="Boosting", value=f"{'True' if user in ctx.guild.premium_subscribers else 'False'}")
    embed.add_field(name="Nickname", value=f"{user.nick}")
    embed.add_field(name="IN-VC", value=f"{'*Not Connected In A Voice Channel*' if not user.voice else user.voice.channel.mention}")
    embed.add_field(name="User Activity", value=f"{'*Nothing*' if not user.activity else user.activity.name}")
    embed.add_field(name="Joined At", value=user.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Join position", value=str(members.index(user)+1))
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ' | '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=True)
    embed.set_author(name=f"{user.name}", icon_url=f"{user.avatar}")
    embed.set_thumbnail(url=user.avatar)
    bannerUser = await bot.fetch_user(user.id)
    if not bannerUser.banner:
      pass
    else:
      embed.set_image(url=bannerUser.banner) 
  
    await ctx.send(embed=embed)
  
@bot.event
async def on_guild_join(guild):
  for x in bot.guilds:
    if x.member_count < 30:
       await guild.owner.send("Cant Join Guild Less Than 30 Member")
       await x.leave()

@bot.event
async def on_command_completion(context: Context) -> None:

    full_command_name = context.command.qualified_name
    split = full_command_name.split(" | ")
    executed_command = str(split[0])
    me = bot.get_channel(1034353367310413874) 
    if context.guild is not None:
        await me.send(
            f"Executed `{executed_command}` command in `{context.guild.name}` (ID: `{context.guild.id}` , 'SERVER NAME: `{context.guild.name}`') by `{context.author}` (ID: `{context.author.id}`)")
    else:
        await me.send(
            f"Executed `{executed_command}` command by `{context.author}` (ID: `{context.author.id}`) in DMs")





def botowner(ctx):
  return ctx.message.author.id == 975012142640169020 or ctx.message.author.id == 985097344880082964


with open('badges.json') as f:
    whitelisted = json.load(f)


@bot.command(aliases=[("ab")])
@commands.check(botowner)
async def add(ctx, user: discord.Member, *, badge):
  if ctx.author.id == 975012142640169020:
    if user is None:
        await ctx.reply(embed=discord.Embed(description="You must specify a user to remove badge"))
        return  
  with open("badges.json", "r") as f:
    idk = json.load(f)
  if str(user.id) not in idk:
    idk[str(user.id)] = []
    idk[str(user.id)].append(f"{badge}")
    await ctx.reply(embed=discord.Embed(description=f"Added badge {badge} to {user}."))
  elif str(user.id) in idk:
    idk[str(user.id)].append(f"{badge}")
    await ctx.reply(embed=discord.Embed(description=f"Added badge {badge} to {user}."))
  with open("badges.json", "w") as f:
    json.dump(idk, f, indent=4)








@bot.command(aliases=["profile", "pr"])
async def badges(ctx, member: discord.Member=None):
  server = ctx.guild
  button = discord.ui.Button(label='Your Badge', style=discord.ButtonStyle.primary)
  button2 = discord.ui.Button(label='Support', style=discord.ButtonStyle.success)
  view = discord.ui.View()
  view.add_item(button)
  view.add_item(button2)
  user = member or ctx.author
  with open("badges.json", "r") as f:
    idk = json.load(f)
  if str(user.id) not in idk:
    async def button_callback(interaction: discord.Interaction):
       embed1 = discord.Embed(title="Oops..!!", description=f"{user} Dont Have Any Badges \n Click below Support button to join the server and have some badges").set_footer(text="Made with 💖 By Proton Developement")
       await interaction.response.edit_message(embed=embed1)
  elif str(user.id) in idk:
    for bd in idk[str(user.id)]:
      embed = discord.Embed(title="Badges", description=f"{bd}").set_thumbnail(url=server.icon.url)
      await ctx.reply(embed=embed)
  async def button2_callback(interaction: discord.Interaction):
    embed9 = discord.Embed(title="Support Server", description="If you dont have any badges \n Click [here](https://discord.gg/A4PpGEG9gB) to join and take")
    await interaction.response.edit_message(embed=embed9)
  avemb = discord.Embed(title="*Click Below The Button To Check Your Badge*")

  button.callback = button_callback
  button2.callback = button2_callback
  await ctx.reply(embed=avemb, view=view)

@commands.check(botowner)
@bot.command(aliases=[("rb")])
async def removeb(ctx, user: discord.User = None):
  if ctx.author.id == 975012142640169020:
    if user is None:
        await ctx.reply(embed=discord.Embed(description="You must specify a user to remove badge"))
        return
    with open('badges.json', 'r') as f:
        badges = json.load(f)
    try:
        if str(user.id) in badges:
            badges.pop(str(user.id))

            with open('badges.json', 'w') as f:
                json.dump(badges, f, indent=4)

            await ctx.reply(embed=discord.Embed(description=f"Removed badge of {user}"))
    except KeyError:
        await ctx.reply("This user has no badge.")


import discord, psutil, pathlib, shutil, os, sys
def get_ram_usage():
    return int(psutil.virtual_memory().total - psutil.virtual_memory().available)


def get_ram_total():
    return int(psutil.virtual_memory().total)



@bot.command(name="info", aliases=['botinfo', 'bi'])
@commands.guild_only()
async def _info(ctx):
    shards_guilds = {i: {"guilds": 0, "users": 0} for i in range(len(ctx.bot.shards))}
    for guild in ctx.bot.guilds:
            shards_guilds[guild.shard_id]["guilds"] += 1
            shards_guilds[guild.shard_id]["users"] += guild.member_count

    p = pathlib.Path('./')
    imp = cm = cr = fn = cl = ls = fc = 0
    for f in p.rglob('*.py'):
            if str(f).startswith("venv"):
                continue
            fc += 1
            with f.open() as of:
                for l in of.readlines():
                    l = l.strip()
                    if l.startswith('class'):
                        cl += 1
                    if l.startswith('def'):
                        fn += 1
                    if l.startswith('import'):
                        imp += 1
                    if l.startswith("from"):
                        imp += 1
                    if l.startswith('async def'):
                        cr += 1
                    if '#' in l:
                        cm += 1
                    ls += 1

    total, used, free = shutil.disk_usage("/")
    embed = discord.Embed(color=discord.Colour(0x2f3136), description=f"""**Developer :** [~ Rao🖤#5461](https://discord.com/users/985097344880082964) \n [⚘ *₊`.𓆩ζ͜͡𝐓he𝐑eal𝐏ennywise٨ـ#1787](https://discord.com/users/975012142640169020)
```adoc\nSupporter :: ~Anay_xD
Created At ::  {ctx.me.created_at}
Guilds :: {len(ctx.bot.guilds):,}
Users :: {len(ctx.bot.users):,}
Commands :: {len(set(ctx.bot.walk_commands()))}
Shards :: {len(ctx.bot.shards)}
Python :: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}```""")
    embed.add_field(name="Storage", value=f"""```yaml\nCPU :: {round(psutil.cpu_percent())}%/100%
RAM :: {int((psutil.virtual_memory().total - psutil.virtual_memory().available)
 / 1024 / 1024)}MB/{int((psutil.virtual_memory().total) / 1024 / 1024)}MB
Disk :: {used // (2 ** 30)}GB/{total // (2 ** 30)}GB
Total Files :: {fc:,}
Functions Defined :: {fn:,}
Total Courtines :: {cr:,}
Total Comments :: {cm:,}```""")
    await ctx.reply(embed=embed, mention_author=False)













link_msg = [
"https://cdn.discordapp.com/attachments/992888603610984478/1003024271712464896/video_20220605_231829_edit.mp4","https://cdn.discordapp.com/attachments/993477049408835614/1003023252228165712/L3OqL1360trTXz9J.mp4","https://media.discordapp.net/attachments/983092347451629628/994908499622498394/VID-20220708-WA0076.mp4","https://media.discordapp.net/attachments/983092347451629628/995408321894961243/VID-20220710-WA0011.mp4","https://media.discordapp.net/attachments/983092347451629628/994338464348766308/video.mov","https://media.discordapp.net/attachments/983092347451629628/995247839003299840/yonautpeedaexclusivesnapreflexx.mp4","https://media.discordapp.net/attachments/983092347451629628/994626732772565093/VID_20220707_205151_062.mp4","https://cdn.discordapp.com/attachments/493460128587055124/993925943888462004/FrostyMintyMillipede-mobile.mp4","https://cdn.discordapp.com/attachments/958731611300585482/990943109078712360/1_5120666722772189452.mp4","https://cdn.discordapp.com/attachments/958731611300585482/975704134445580359/1_5167943313289904686.mp4","https://media.discordapp.net/attachments/983092347451629628/995774849651855460/yonutpeedanexclusive.mp4","https://media.discordapp.net/attachments/983092347451629628/995808527648043018/yonutpeedanexclusive.mp4","https://cdn.discordapp.com/attachments/936300178426720336/940173688119107584/bandicam_2021-10-19_10-18-57-222.mp4","https://media.discordapp.net/attachments/964407026857934899/989452922389663774/VID-20220604-WA0005.mp4","https://cdn.discordapp.com/attachments/989174758807580793/989467029780181002/VID-20220323-WA0020.mp4","https://thumbs2.redgifs.com/VillainousMidnightblueIsabellineshrike-mobile.mp4#t=0","https://cdn.discordapp.com/attachments/988306082097143860/994089750396932157/IMG_20220114_002710_266.mp4","https://media.discordapp.net/attachments/989624707252879421/991434651036024922/14014ce76ef11f57.mp4","https://media.discordapp.net/attachments/989624707252879421/991448226249048074/received_2858213127809144.mp4","https://media.discordapp.net/attachments/1002608922147950603/1002611818822369371/VID-20220715-WA0058_1.mp4","https://media.discordapp.net/attachments/979483411477565480/1004873258274922516/VID_398041215_084645_548.mp4","https://media.discordapp.net/attachments/1002612089896042587/1002612260474204230/VID_63210110_152259_646.mp4","https://media.discordapp.net/attachments/999999557872144424/1004685375647793252/VID_153220912_004901_192.mp4","https://media.discordapp.net/attachments/1006565622165028864/1006597476876288162/IMG_2189.mp4","https://media.discordapp.net/attachments/1006565622165028864/1006616635395801088/WhatsApp_Video_2022-08-09_at_10.30.37_PM.mp4","https://media.discordapp.net/attachments/1006565622165028864/1006597475764801586/Snapchat-1821935123.mp4","https://media.discordapp.net/attachments/1006565622165028864/1006589065161867415/WhatsApp_Video_2022-08-09_at_8.03.38_PM.mp4","https://media.discordapp.net/attachments/1006565622165028864/1006590655151214643/VID_20220624_175051_385.mp4","https://media.discordapp.net/attachments/1006565622165028864/1006572977120346163/DUFilManager.mp4","https://media.discordapp.net/attachments/1006565622165028864/1006572978701615125/gawd_rules22.mp4","https://media.discordapp.net/attachments/1006565622165028864/1006573019914842222/gawd_rules28.mp4","https://media.discordapp.net/attachments/1006565622165028864/1006569461383442474/I7vqEOw7_480p.mp4","https://media.discordapp.net/attachments/1006565622165028864/1006569462356512788/12370.mp4","https://media.discordapp.net/attachments/1006565622165028864/1006569462356512788/12370.mp4","https://media.discordapp.net/attachments/1006565622165028864/1006569850656788653/Dream_Alone_7.mp4","https://media.discordapp.net/attachments/1006565622165028864/1006568394625130556/VID-20220716-WA0028.mp4","https://media.discordapp.net/attachments/1006565622165028864/1006568069151346788/11.mp4","https://media.discordapp.net/attachments/1006565622165028864/1006568065577779230/VID_20220704_012126.mp4","https://cdn.discordapp.com/attachments/986376783966371910/986389655433908324/Nudehub_7.mp4", "https://cdn.discordapp.com/attachments/986376783966371910/986389655844962374/Nudehub_8.mov","https://cdn.discordapp.com/attachments/986376783966371910/986389656608338101/Nudehub_9.mp4","https://cdn.discordapp.com/attachments/986376783966371910/986389657245843506/Nudehub_10.mp4",
"https://cdn.discordapp.com/attachments/986376783966371910/986389657778540554/Nudehub_1.mov",
"https://cdn.discordapp.com/attachments/986376783966371910/986389658495778887/Nudehub_2.mp4",
"https://cdn.discordapp.com/attachments/986376783966371910/986389658822901790/Nudehub_3.mov",
"https://cdn.discordapp.com/attachments/986376783966371910/986389659242336266/Nudehub_4.mp4",
"https://cdn.discordapp.com/attachments/986376783966371910/986389659955380364/Nudehub_5.mov",
"https://cdn.discordapp.com/attachments/986376783966371910/986389660257366086/Nudehub_6.mov",
"https://cdn.discordapp.com/attachments/986376783966371910/986389800829456394/Nudehub_16.mp4",
"https://cdn.discordapp.com/attachments/986376783966371910/986389801768976454/Nudehub_17.mp4",
"https://cdn.discordapp.com/attachments/986376820557512764/986386175596044349/video_2021-07-30_20-41-54.mp4",
"https://cdn.discordapp.com/attachments/986376820557512764/986386154070892614/video_2021-07-30_20-51-24.mp4",
"https://cdn.discordapp.com/attachments/986376820557512764/986386115781074964/video_2021-07-30_20-42-23.mp4",
"https://cdn.discordapp.com/attachments/986376820557512764/986386114044637214/video_2021-07-30_20-49-34.mp4",
"https://cdn.discordapp.com/attachments/986376820557512764/986386113134489620/video_2021-07-30_20-52-55.mp4",
"https://cdn.discordapp.com/attachments/986376820557512764/986386110705975316/4f86ed8ce80e0811.mp4",
"https://cdn.discordapp.com/attachments/986376820557512764/986386108478808114/video_2021-07-30_20-45-29.mp4",
"https://cdn.discordapp.com/attachments/986376820557512764/986385705372647494/video_2021-08-15_03-32-13.mp4",
"https://cdn.discordapp.com/attachments/986376820557512764/986385628000321616/video_2021-07-30_20-52-15.mp4",
"https://cdn.discordapp.com/attachments/986376820557512764/986385442242977912/IMG_3256.mp4",
"https://cdn.discordapp.com/attachments/986376880728969306/988072241789026314/Nudehub_54.mp4",
"https://cdn.discordapp.com/attachments/986376880728969306/988072217273307206/Nudehub_53.mp4",
"https://cdn.discordapp.com/attachments/986376880728969306/988072189179875349/Nudehub_52.mp4",
"https://cdn.discordapp.com/attachments/986376880728969306/988072166023122965/Nudehub_51.mp4",
"https://cdn.discordapp.com/attachments/986376880728969306/988072147979223060/Nudehub_50.mp4",
"https://cdn.discordapp.com/attachments/986376880728969306/988072137782886430/Nudehub_49.mp4",
"https://cdn.discordapp.com/attachments/986376880728969306/988072099996397608/Nudehub_48.mp4",
"https://cdn.discordapp.com/attachments/986376880728969306/988071991292624946/Nudehub_44.mp47.mp4",
"https://cdn.discordapp.com/attachments/986376880728969306/988071975043874856/Nudehub_43.mp4",
"https://cdn.discordapp.com/attachments/986376906091933696/986389170584948736/0421.mp4",
"https://cdn.discordapp.com/attachments/986376906091933696/986389158853488650/1.mp4",
"https://cdn.discordapp.com/attachments/986376906091933696/986389139572260934/2_5411543026411507456.mp4",
"https://cdn.discordapp.com/attachments/986376906091933696/986389113030725672/Creampie_Porn_GIFs_on_xCafe_-_page_12.mp4",
"https://cdn.discordapp.com/attachments/986376906091933696/986389100791734342/916172.mp4",
"https://cdn.discordapp.com/attachments/986376906091933696/986389052506918922/3zpJQuR5oV7phH1K.mp4",
"https://cdn.discordapp.com/attachments/986376906091933696/986389046110588998/1001284.mp4",
"https://cdn.discordapp.com/attachments/986376906091933696/986389034051989634/video_2021-07-30_20-52-03.mp4",
"https://cdn.discordapp.com/attachments/986376906091933696/986388994705219665/d84873d37ea8aa1bceefd9042caaee1b.mov",
"https://cdn.discordapp.com/attachments/986377010152620082/986620648010960969/Nudehub_19.mp4",
"https://cdn.discordapp.com/attachments/986377010152620082/986620646664577104/Nudehub_18.mp4",
"https://cdn.discordapp.com/attachments/986377010152620082/986620636321419364/Nudehub_21.mp4",
"https://cdn.discordapp.com/attachments/986377010152620082/986620634417217556/Nudehub_20.mp4",
"https://cdn.discordapp.com/attachments/986377010152620082/986619897389912094/Nudehub_16.mp4",
"https://cdn.discordapp.com/attachments/986376549844520991/986380247689752617/26354102a.webm",
"https://cdn.discordapp.com/attachments/986376549844520991/986380247224180756/8b236673-07ab-4a11-8a12-3ba390acb7cc.mp4",
"https://cdn.discordapp.com/attachments/986376549844520991/986380246485966908/965171a.webm",
"https://cdn.discordapp.com/attachments/986376549844520991/986380245567438868/8031441a.webm",
"https://cdn.discordapp.com/attachments/986376549844520991/986380245114449981/15042882a.webm",
"https://cdn.discordapp.com/attachments/986376549844520991/986380243927457832/8a54acc661bf551cc428b98273d49f21.mp4",
"https://cdn.discordapp.com/attachments/986376549844520991/986380243042435132/2_5339059448927225076.mp4",
"https://cdn.discordapp.com/attachments/986376549844520991/986380242388156436/3f88153d-37ff-4ce6-9710-46abddb4ecd4.mp4",
"https://cdn.discordapp.com/attachments/986376549844520991/986380241758994452/4_5992105214784571524_1.mp4","https://media.discordapp.net/attachments/1014055797795340318/1016696551738978404/VID_20220906_183223_123.mp4","https://media.discordapp.net/attachments/1014055797795340318/1016696548702302278/VID_20220906_183158_669.mp4","https://cdn.discordapp.com/attachments/985428944562028564/1016772711860678667/trim.2B5F8930-503B-436B-9A6B-6147D08283D1.mov",
"https://cdn.discordapp.com/attachments/985428944562028564/1016697366725804073/trim.C655B88F-3B27-4373-9A4B-84946C75283B.mp4",
"https://cdn.discordapp.com/attachments/977277313723027497/1018214835437179113/VID_173530302_130440_169.mp4",
"https://cdn.discordapp.com/attachments/977277313723027497/1018214834971615333/VID_173520412_055000_336.mp4",
"https://cdn.discordapp.com/attachments/977277313723027497/1018214834506051596/VID_173511031_020347_164.mp4",
"https://cdn.discordapp.com/attachments/977277313723027497/1018214833352622180/VID_30520622_115130_197.mp4",
"https://cdn.discordapp.com/attachments/977277313723027497/1018214755179171960/VID_20220324_001003_629.mp4",
"https://cdn.discordapp.com/attachments/993452077244219403/1002554606225727581/sp_47.mp4",
"https://cdn.discordapp.com/attachments/977277344119132160/996738375899955322/TT170_360.mp4",
"https://cdn.discordapp.com/attachments/977277344119132160/996738375132389426/1620750489.7295_115499611_360.mp4",
"https://cdn.discordapp.com/attachments/977277344119132160/996738226985369680/TT632_360.mp4",
"https://cdn.discordapp.com/attachments/977277344119132160/996738202725523496/ShimmeringPhysicalChamois.mp4",
"https://cdn.discordapp.com/attachments/977277344119132160/996736066931408937/AzureDampNerka.mp4",
"https://cdn.discordapp.com/attachments/977277344119132160/996736065505337437/2022-05-02_11-00-31_1_360.mp4",
"https://cdn.discordapp.com/attachments/979285555286274068/997831924645118043/Donette07230129_720x1210_1471329114112020483.mp4",
"https://cdn.discordapp.com/attachments/979285555286274068/997831452727185438/GtN0259.mp4",
]

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.channel)
async def nsfw(ctx):
  if ctx.channel.is_nsfw() != True:
    icon_url= "https://support.discord.com/hc/article_attachments/4580654542103/unnamed.png"
    await ctx.reply(embed=discord.Embed(description="Please enable this in your channel").set_image(url=icon_url).set_thumbnail(url=ctx.author.display_avatar.url))
  else:
    await ctx.reply(f"{random.choice(link_msg)}", mention_author=True)

@bot.event
@commands.cooldown(1, 5, commands.BucketType.channel)
async def on_command_error(ctx, error) -> None:

    if isinstance(error, commands.CommandNotFound):
      return
    if isinstance(error, commands.DisabledCommand):
        embed = discord.Embed(
            title="Error!",
            description="Command has been disabled",
            color=0x2F3136
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0x2F3136
        )
        await ctx.send(embed=embed)
    elif isinstance(error, exceptions.UserBlacklisted):
        embed = discord.Embed(
            title="Error!",
            description="You are blacklisted from using the bot.",
            color=0x2F3136
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.NoPrivateMessage):
      await ctx.send("You Can't Use My Commands In Dm")
    elif isinstance(error, exceptions.UserNotOwner):
        embed = discord.Embed(
            title="Error!",
            description="You are not the owner of the bot!",
            color=0x2F3136
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            title="Error!",
            description="Could Not Find That Member \n Try Again",
            color=0x2F3136
        )
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to execute this command!",
            color=0x2F3136
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            description="Are You Missing Some Rqt?",
            color=0x2F3136
        )
        await ctx.send(embed=embed)
    raise error  

if __name__ == '__main__':
    init_db()
    asyncio.run(load_cogs())
    bot.run()


#put your token in /core/bot.py not here
    