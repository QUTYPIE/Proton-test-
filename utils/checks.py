import json
from discord.ext import commands
import time
import asyncio


def getConfig(guildID):
    with open("database/config.json", "r") as config:
        data = json.load(config)
    if str(guildID) not in data["guilds"]:
        defaultConfig = {
            "whitelist": [],
            "log_channel": None,
            "wlrole": None,
            "owner": [],
            "backupkey": "",
            "autorole": [],
            "bots": [],
            "humans": [],
            "message": "",
            "channel": None,
            "wen": False,
            "vcrole": [],
            "staff": None,
            "vip": None,
            "girl": None,
            "guest": None,
            "frnd": None,
            "clowns": None,
            "art": None
        }
        updateConfig(guildID, defaultConfig)
        return defaultConfig
    return data["guilds"][str(guildID)]


def updateConfig(guildID, data):
    with open("database/config.json", "r") as config:
        config = json.load(config)
    config["guilds"][str(guildID)] = data
    newdata = json.dumps(config, indent=4, ensure_ascii=False)
    with open("database/config.json", "w") as config:
        config.write(newdata)



def guild_owner_only():
    async def predicate(ctx):
      guild = ctx.guild
      g = getConfig(guild.id)
      owner = g['owner']
      return ctx.author == ctx.guild.owner or ctx.author in owner
    return commands.check(predicate)
