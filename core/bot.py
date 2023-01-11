from __future__ import annotations
import motor.motor_asyncio as motor
import discord
from discord.ext import commands, tasks
import traceback
from pymongo import UpdateOne
import jishaku
import random
import json
import asyncio
import os
import aiohttp
import time
from utils.embed import success_embed
from utils.ui import DropDownSelfRoleView, ButtonSelfRoleView
from cogs.ticket import createTicket, closeTicket

os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ['JISHAKU_EMBEDDED_JSK'] = "True"

TOKEN = "MTAyNzQyODA4ODU2MjMxOTM5MQ.GPJhE5.gJ-AWU6gjv51V8P_XNkvCEYsooEw9Nb7CsM9As" # add the token and run the bot
MONGO_DB_URL = "mongodb+srv://hacker:chetan2004@cluster0.rxh8r.mongodb.net/?retryWrites=true&w=majority"

OWNERS = [
  985097344880082964,
  975012142640169020
]

class Bot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
          command_prefix=self.get_prefix,
          case_insensitive=True,
          intents=discord.Intents.all(),
          help_command=None,
          owner_ids=OWNERS,
          strip_after_prefix=True,
          allowed_mentions=discord.AllowedMentions(
            everyone=False,
            replied_user=False,
            roles=False
          )
        )
        self._BotBase__cogs = commands.core._CaseInsensitiveDict()
        cluster = motor.AsyncIOMotorClient(MONGO_DB_URL)
        self.session = aiohttp.ClientSession()

      
        self.cache_loaded = False
        self.cogs_loaded = False
        self.views_loaded = False
        self.rolemenus_loaded = False

        self.last_updated_serverconfig_db = 0

        self.db = cluster['Protondb']
        self.serverconfig = self.db['serverconfig']
        self.self_roles = self.db['self_roles']


        self.serverconfig_cache = []
        self.persistent_views_added = False

        
       
      
    async def set_default_guild_config(self, guild_id):
        pain = {
            "_id": guild_id,
            "counters": {"members": None, "huamns": None, "bots": None, "channels": None, "categories": None, "roles": None, "emojis": None}
        }
        self.serverconfig_cache.append(pain)
        return await self.get_guild_config(guild_id)

    async def get_guild_config(self, guild_id):
        for e in self.serverconfig_cache:
            if e['_id'] == guild_id:
                if "counters" not in e:
                    e.update({"counters": {"members": None, "huamns": None, "bots": None, "channels": None, "categories": None, "roles": None, "emojis": None}})
                return e
        return await self.set_default_guild_config(guild_id)      
    

    @tasks.loop(seconds=10, reconnect=True)
    async def update_serverconfig_db(self):
            cancer = []
            for eee in self.serverconfig_cache:
                hmm = UpdateOne(
                    {"_id": eee['_id']},
                    {"$set": {
                        "counters": {"members": None, "huamns": None, "bots": None, "channels": None, "categories": None, "roles": None, "emojis": None} if "counters" not in eee else eee['counters']
                    }},
                    upsert=True
                )
                cancer.append(hmm)
            if len(cancer) != 0:
                await self.serverconfig.bulk_write(cancer)
            self.last_updated_serverconfig_db = time.time()  

    @update_serverconfig_db.before_loop
    async def before_update_serverconfig_db(self):
        await self.wait_until_ready()

    async def get_cache(self):
      
        cursor = self.serverconfig.find({})
        self.serverconfig_cache = await cursor.to_list(length=None)
        print(f"Server config cache has been loaded. | {len(self.serverconfig_cache)} configs")

    async def load_rolemenus(self, dropdown_view, button_view):
        i = 0
        cursor = self.self_roles.find({})
        h = await cursor.to_list(length=None)
        for amogus in h:
            guild = self.get_guild(amogus['_id'])
            if guild is not None:
                role_menus = amogus['role_menus']
                for msg_id, menu in role_menus.items():
                    if menu['type'] == 'dropdown':
                        self.add_view(dropdown_view(guild, menu['stuff']), message_id=int(msg_id))
                        i += 1
                    if menu['type'] == 'button':
                        self.add_view(button_view(guild, menu['stuff']), message_id=int(msg_id))
                        i += 1
        self.rolemenus_loaded = True

        print(f"Self role views has been loaded. | {i} views")
  
  
    @tasks.loop(minutes=1.0)
    async def status_task(self) -> None:
      statuses = ["Proton", "Heaven For Users", "Fastest", "Hell For Nukers", "-help"]
      await self.change_presence(activity=discord.Game(random.choice(statuses)))

    async def on_ready(self) -> None:
      print("Connected as {}".format(self.user))
      if not self.rolemenus_loaded:
            await self.load_rolemenus(DropDownSelfRoleView, ButtonSelfRoleView)
      if not self.persistent_views_added:
            self.add_view(createTicket())
            self.add_view(closeTicket())
            self.persistent_views_added = True
         
      self.status_task.start()  
      self.update_serverconfig_db.start()

    async def get_prefix(self, message: discord.Message):
        with open('database/prefix.json', 'r') as f:
          p = json.load(f)
        if message.author.id in p["non_prefix"]:  
          return commands.when_mentioned_or('-','')(self, message)
        else:
          return commands.when_mentioned_or('-')(self, message)

    def run(self) -> None:
        super().run(TOKEN, reconnect=True)











        