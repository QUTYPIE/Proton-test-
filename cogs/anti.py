import os
import discord
import pymongo
import aiohttp
import logging
import datetime
import requests
from discord.ext import commands, tasks
from utils.checks import getConfig, updateConfig
from discord.colour import Color




IGNORE = (
  985097344880082964,
  975012142640169020,
)

emoji = "<:arrow:1040656090687361024>"

class Anti(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.processing = [
            
        ]

    @tasks.loop(seconds=15)
    async def clean_processing(self):
        self.processing.clear()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.clean_processing.start()

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member,
                               after: discord.Member) -> None:
        await self.bot.wait_until_ready()        
        guild = after.guild
        g = getConfig(guild.id) 
        wl = g['whitelist']#
        wlrole = g['wlrole']              
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in after.guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.member_role_update):
            if entry.user.id == guild.owner.id:
                  return
            if entry.user.id in IGNORE: 
                  return
            if entry.user.id in wl:
                  return
            mem = guild.get_member(entry.user.id)  
            wlrole = guild.get_role(wlrole)
            if wlrole in mem.roles:
                  return
            else:
              for role in after.roles:
                  if role not in before.roles:
                    if role.permissions.administrator or role.permissions.manage_guild or role.permissions.kick_members or role.permissions.ban_members:
                       if guild.me.guild_permissions.ban_members:
                          reason = "Proton | Anti Member Role Update"
                          await guild.ban(entry.user,
                                   reason=reason)                
                          await after.remove_roles(role)  

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user) -> None:
        await self.bot.wait_until_ready()
        g = getConfig(guild.id) 
        wl = g['whitelist']#
        wlrole = g['wlrole']   
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.now() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.ban):
            if entry.user.id == guild.owner.id:
                  return
            if entry.user.id in IGNORE: 
                  return
            if entry.user.id in wl:
                  return
            mem = guild.get_member(entry.user.id)  
            wlrole = guild.get_role(wlrole)
            if wlrole in mem.roles:
                  return
            else:
                if guild.me.guild_permissions.ban_members:
                    reason = "Proton | Anti Ban"
                    user = entry.user
                    await guild.ban(entry.user,
                                   reason=reason)

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild,
                              user: discord.User) -> None:
        await self.bot.wait_until_ready()
        g = getConfig(guild.id) 
        wl = g['whitelist']#
        wlrole = g['wlrole']   
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.unban):
            if entry.user.id == guild.owner.id:
                  return
            if entry.user.id in IGNORE: 
                  return
            if entry.user.id in wl:
                  return
            mem = guild.get_member(entry.user.id)  
            wlrole = guild.get_role(wlrole)
            if wlrole in mem.roles:
                  return
            else:
                if guild.me.guild_permissions.ban_members:
                    reason = "Proton | Anti Unban"
                    user = entry.user
                    await guild.ban(entry.user,
                                   reason=reason)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        await self.bot.wait_until_ready()
        guild = member.guild
        g = getConfig(guild.id) 
        wl = g['whitelist']#
        wlrole = g['wlrole']       
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.kick):
            if entry.user.id == guild.owner.id:
                  return
            if entry.user.id in IGNORE: 
                  return
            if entry.user.id in wl:
                  return
            mem = guild.get_member(entry.user.id)  
            wlrole = guild.get_role(wlrole)
            if wlrole in mem.roles:
                  return
            else:
                if guild.me.guild_permissions.ban_members:
                    reason = "Proton | Anti Kick"
                    user = entry.user
                    await guild.ban(entry.user,
                                   reason=reason)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        await self.bot.wait_until_ready()

        guild = member.guild
        g = getConfig(guild.id) 
        wl = g['whitelist']#
        wlrole = g['wlrole']   
        logchannel = self.bot.get_channel(g['log_channel'])         
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.bot_add):
            if entry.user.id == guild.owner.id:
                  return
            if entry.user.id in IGNORE: 
                  return
            if entry.user.id in wl:
                  return
            mem = guild.get_member(entry.user.id)  
            wlrole = guild.get_role(wlrole)
            if wlrole in mem.roles:
                  return
            if member.bot:
                await member.ban(reason="Proton | Anti Bot")
                if guild.me.guild_permissions.ban_members:
                    reason = "Proton | Anti Bot"
                    user = entry.user
                    await guild.ban(entry.user,
                                   reason=reason)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel) -> None:
        await self.bot.wait_until_ready()

        guild = channel.guild
        g = getConfig(guild.id) 
        wl = g['whitelist']#
        wlrole = g['wlrole']   
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.channel_create):
            if entry.user.id == guild.owner.id:
                  return
            if entry.user.id in IGNORE: 
                  return
            if entry.user.id in wl:
                  return
            mem = guild.get_member(entry.user.id)  
            wlrole = guild.get_role(wlrole)
            if wlrole in mem.roles:
                  return
            else:                
                if guild.me.guild_permissions.ban_members:
                    reason = "Proton | Anti Channel Create"
                    user = entry.user
                    await guild.ban(entry.user,
                                   reason=reason)
                await entry.channel.delete()
                await entry.channel.delete()
                await entry.channel.delete()
                await entry.channel.delete()

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel) -> None:
        await self.bot.wait_until_ready()

        guild = channel.guild
        g = getConfig(guild.id) 
        wl = g['whitelist']#
        wlrole = g['wlrole']       
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.channel_delete):
            if entry.user.id == guild.owner.id:
                  return
            if entry.user.id in IGNORE: 
                  return
            if entry.user.id in wl:
                  return
            mem = guild.get_member(entry.user.id)  
            wlrole = guild.get_role(wlrole)
            if wlrole in mem.roles:
                  return
            else:
                if guild.me.guild_permissions.ban_members:
                    reason = "Proton | Anti Channel Delete"
                    user = entry.user
                    await guild.ban(entry.user,
                                   reason=reason)
                    await channel.clone()
                    await channel.clone()

    #@commands.Cog.listener()
    #async def on_guild_channel_update(
            #self, after: discord.abc.GuildChannel,
            #before: discord.abc.GuildChannel) -> None:
        #await self.bot.wait_until_ready()

        #name = before.name
       # guild = after.guild
        #g = getConfig(guild.id) 
        #wl = g['whitelist']#
        #wlrole = g['wlrole']                 
        #if not guild:
          #  return

        #async for entry in guild.audit_logs(
          #      limit=1,
            #    after=datetime.datetime.now() - datetime.timedelta(minutes=2),
          #      action=discord.AuditLogAction.channel_update):
          #  if entry.user.id == guild.owner.id:
           #       return
           # if entry.user.id in IGNORE: 
            #      return
          #  if entry.user.id in wl:
          #        return
         #   if entry.user.top_role >= guild.me.top_role:
          #        return
           # mem = guild.get_member(entry.user.id)  
            #wlrole = guild.get_role(wlrole)
        #    if wlrole in mem.roles:
         #         return
          #  else:
           #     
            #    if guild.me.guild_permissions.ban_members:
             #       reason = "Proton | Anti Channel Update"
              #      user = entry.user
               #     await guild.ban(entry.user,
                #                   reason=reason)
                #await after.edit(name=f"{name}", reason=f"Proton | Recovery")  

    @commands.Cog.listener()
    async def on_guild_update(self, after: discord.Guild,
                              before: discord.Guild) -> None:
        await self.bot.wait_until_ready()

        guild = after
        g = getConfig(guild.id) 
        wl = g['whitelist']#
        wlrole = g['wlrole']                 
        if not guild:
            return

        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.guild_update):
            if entry.user.id == guild.owner.id:
                  return
            if entry.user.id in IGNORE: 
                  return
            if entry.user.id in wl:
                  return
            mem = guild.get_member(entry.user.id)  
            wlrole = guild.get_role(wlrole)
            if wlrole in mem.roles:
                  return
            else:
                
                if guild.me.guild_permissions.ban_members:
                    reason = "Proton | Anti Guild Update"
                    user = entry.user
                    await guild.ban(entry.user,
                                   reason=reason)
                await after.edit(name=f"{before.name}",
                                 reason="Proton | Recovery")  

    @commands.Cog.listener()
    async def on_webhooks_update(self, channel) -> None:
        await self.bot.wait_until_ready()

        guild = channel.guild
        g = getConfig(guild.id) 
        wl = g['whitelist']#
        wlrole = g['wlrole']        
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.webhook_create):
            if entry.user.id == guild.owner.id:
                  return
            if entry.user.id in IGNORE: 
                  return
            if entry.user.id in wl:
                  return
            mem = guild.get_member(entry.user.id)  
            wlrole = guild.get_role(wlrole)
            if wlrole in mem.roles:
                  return
            else:
                webhooks = await guild.webhooks()
                for webhook in webhooks:
                    if webhook.id == entry.target.id:
                        if guild.me.guild_permissions.manage_webhooks:
                            await webhook.delete()
                            break
                if guild.me.guild_permissions.ban_members:
                    reason = "Proton | Anti Webhook"
                    user = entry.user
                    await guild.ban(entry.user,
                                   reason=reason)
                webhooks = await guild.webhooks()
                for webhook in webhooks:
                    if webhook.id == entry.target.id:
                        if guild.me.guild_permissions.manage_webhooks:
                            await webhook.delete()
                            break  

    @commands.Cog.listener()
    async def on_guild_role_create(self, role) -> None:
        await self.bot.wait_until_ready()

        guild = role.guild
        g = getConfig(guild.id) 
        wl = g['whitelist']#
        wlrole = g['wlrole']        
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.role_create):
            if entry.user.id == guild.owner.id:
                  return
            if entry.user.id in IGNORE: 
                  return
            if entry.user.id in wl:
                  return
            mem = guild.get_member(entry.user.id)  
            wlrole = guild.get_role(wlrole)
            if wlrole in mem.roles:
                  return
            else:
                await role.delete()
                if guild.me.guild_permissions.ban_members:
                    reason = "Proton | Anti Role Create"
                    user = entry.user
                    await guild.ban(entry.user,
                                   reason=reason)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role) -> None:
        await self.bot.wait_until_ready()

        guild = role.guild
        g = getConfig(guild.id) 
        wl = g['whitelist']#
        wlrole = g['wlrole']         
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.role_delete):
            if entry.user.id == guild.owner.id:
                  return
            if entry.user.id in IGNORE: 
                  return
            if entry.user.id in wl:
                  return
            mem = guild.get_member(entry.user.id)  
            wlrole = guild.get_role(wlrole)
            if wlrole in mem.roles:
                  return
            else:
                await role.clone()
                if guild.me.guild_permissions.ban_members:
                    reason = "Proton | Anti Role Delete"
                    user = entry.user
                    await guild.ban(entry.user,
                                   reason=reason)

    @commands.Cog.listener()
    async def on_guild_role_update(self, after: discord.Role,
                                   before: discord.Role) -> None:
        await self.bot.wait_until_ready()

        guild = after.guild
        g = getConfig(guild.id) 
        wl = g['whitelist']#
        wlrole = g['wlrole']                               
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        async for entry in guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.role_update):
            if entry.user.id == guild.owner.id:
                  return
            if entry.user.id in IGNORE: 
                  return
            if entry.user.id in wl:
                  return
            mem = guild.get_member(entry.user.id)  
            wlrole = guild.get_role(wlrole)
            if wlrole in mem.roles:
                  return
            else:
                permissions = before.permissions
                name = before.name
                await after.edit(name=name, permissions=permissions)
                if guild.me.guild_permissions.ban_members:
                    reason = "Proton | Anti Role Update"
                    user = entry.user
                    await guild.ban(entry.user,
                                   reason=reason)


async def setup(bot):
	await bot.add_cog(Anti(bot))