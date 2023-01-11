import random
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from helpers import checks
from utils.checks import getConfig, updateConfig

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """Roles commands"""

    def help_custom(self):
		      emoji = '<:server:1040652932829433876>'
		      label = "Server Roles"
		      description = "Shows all Roles Commands"
		      return emoji, label, description   

    async def add_role(self, *, role: int, member: discord.Member):
        if member.guild.me.guild_permissions.manage_roles:
            role = discord.Object(id=int(role))
            await member.add_roles(role, reason="Apolex | Role Added ")  

    async def remove_role(self, *, role: int, member: discord.Member):
        if member.guild.me.guild_permissions.manage_roles:
            role = discord.Object(id=int(role))
            await member.remove_roles(role, reason="Apolex | Role Removed") 

      

    @commands.hybrid_group(
        name="set",
        description="set roles",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    async def set(self, context: Context):
        ...

    @set.command(
      name = "staff",
      description="sets staff role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def staff(self, context: Context, role: discord.Role) -> None:
        if data := getConfig(context.guild.id):

              data['staff'] = role.id
              updateConfig(context.guild.id, data)
              embed = discord.Embed(
                      description=f"{role.mention} Has set to staff role",
                      color=0x01f5b6
              )
              await context.send(embed=embed) 

    @set.command(
      name = "girl",
      description="sets girl role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def girl(self, context: Context, role: discord.Role) -> None:
        if data := getConfig(context.guild.id):

              data['girl'] = role.id
              updateConfig(context.guild.id, data)
              embed = discord.Embed(
                      description=f"{role.mention} Has set to girl role",
                      color=0x01f5b6
              )
              await context.send(embed=embed)           

    @set.command(
      name = "vip",
      description="sets vip role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def vip(self, context: Context, role: discord.Role) -> None:
        if data := getConfig(context.guild.id):

              data['vip'] = role.id
              updateConfig(context.guild.id, data)
              embed = discord.Embed(
                      description=f"{role.mention} Has set to vip role",
                      color=0x01f5b6
              )
              await context.send(embed=embed) 

    @set.command(
      name = "guest",
      description="sets guest role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def guest(self, context: Context, role: discord.Role) -> None:
        if data := getConfig(context.guild.id):

              data['guest'] = role.id
              updateConfig(context.guild.id, data)
              embed = discord.Embed(
                      description=f"{role.mention} Has set to guest role",
                      color=0x01f5b6
              )
              await context.send(embed=embed)  

    @set.command(
      name = "friend",
      description="sets friend role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def friend(self, context: Context, role: discord.Role) -> None:
        if data := getConfig(context.guild.id):

              data['frnd'] = role.id
              updateConfig(context.guild.id, data)
              embed = discord.Embed(
                      description=f"{role.mention} Has set to friend role",
                      color=0x01f5b6
              )
              await context.send(embed=embed)           

    @set.command(
      name = "clown",
      description="sets clown role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def clown(self, context: Context, role: discord.Role) -> None:
        if data := getConfig(context.guild.id):

              data['clowns'] = role.id
              updateConfig(context.guild.id, data)
              embed = discord.Embed(
                      description=f"{role.mention} Has set to clown role",
                      color=0x01f5b6
              )
              await context.send(embed=embed) 

    @set.command(
      name = "artist",
      description="sets artist role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="Role to be added")
    async def artist(self, context: Context, role: discord.Role) -> None:
        if data := getConfig(context.guild.id):

              data['art'] = role.id
              updateConfig(context.guild.id, data)
              embed = discord.Embed(
                      description=f"{role.mention} Has set to artist role",
                      color=0x01f5b6
              )
              await context.send(embed=embed) 
  
    @commands.hybrid_group(
        name="give",
        description="give roles",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    async def give(self, context: Context):
        ...

    @give.command(
      name = "staff",
      description="give staff role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to give staff")
    async def givestaff(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
              role = data['staff']
              await self.add_role(role=role, member=member)
              embed = discord.Embed(
                      description=f"{member.mention} Has given staff",
                      color=0x01f5b6
              )
              await context.send(embed=embed) 

    @give.command(
      name = "girl",
      description="give girl role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to give girl")
    async def givegirl(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
              role = data['girl']
              await self.add_role(role=role, member=member)
              embed = discord.Embed(
                      description=f"{member.mention} Has given girl",
                      color=0x01f5b6
              )
              await context.send(embed=embed)         

    @give.command(
      name = "vip",
      description="give vip role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to give vip")
    async def gvip(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
              role = data['vip']
              await self.add_role(role=role, member=member)
              embed = discord.Embed(
                      description=f"{member.mention} Has given vip",
                      color=0x01f5b6
              )
              await context.send(embed=embed)  

    @give.command(
      name = "guest",
      description="give guest role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to give guest")
    async def giveguest(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
              role = data['guest']
              await self.add_role(role=role, member=member)
              embed = discord.Embed(
                      description=f"{member.mention} Has given guest",
                      color=0x01f5b6
              )
              await context.send(embed=embed) 

    @give.command(
      name = "friend",
      description="give friend role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to give friend")
    async def givefriend(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
              role = data['frnd']
              await self.add_role(role=role, member=member)
              embed = discord.Embed(
                      description=f"{member.mention} Has given friend",
                      color=0x01f5b6
              )
              await context.send(embed=embed)        
          

    @give.command(
      name = "clown",
      description="give clown role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to give clown")
    async def giveclown(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
              role = data['clowns']
              await self.add_role(role=role, member=member)
              embed = discord.Embed(
                      description=f"{member.mention} Has given clown",
                      color=0x01f5b6
              )
              await context.send(embed=embed)   

    @give.command(
      name = "artist",
      description="give artist role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to give artist")
    async def giveart(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
              role = data['art']
              await self.add_role(role=role, member=member)
              embed = discord.Embed(
                      description=f"{member.mention} Has given artist",
                      color=0x01f5b6
              )
              await context.send(embed=embed)   

    @commands.hybrid_group(
        name="show",
        description="show roles",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    async def show(self, context: Context):
        ...

    @show.command(
      name = "roles",
      description="show all cstm assined roles",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    async def rsta(self, context: Context) -> None:
        if data := getConfig(context.guild.id):
              staff = data['staff']
              girl = data['girl']
              vip = data['vip']
              guest = data['guest']
              clown = data['clowns']
              artist = data['art']
              friends = data['frnd']
              
              embed = discord.Embed(title=f"{context.guild.name}",
                      description=f"**Staff** -> <@&{staff}>\n**Girl** -> <@&{girl}>\n**Vip** -> <@&{vip}>\n**Guest** -> <@&{guest}>\n**Clown** -> <@&{clown}>\n**Artist** -> <@&{artist}>\n**Friend** -> <@&{friends}>",
                      color=0x01f5b6
              )
              await context.send(embed=embed) 
    @commands.hybrid_group(
        name="remove",
        description="remove roles",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    async def remove(self, context: Context):
        ...

    @remove.command(
      name = "staff",
      description="remove staff role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to remove staff")
    async def rstaff(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
              role = data['staff']
              await self.remove_role(role=role, member=member)
              embed = discord.Embed(
                      description=f"{member.mention} Has Removed From staff",
                      color=0x01f5b6
              )
              await context.send(embed=embed) 

    @remove.command(
      name = "girl",
      description="remove girl role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to remove girl")
    async def rgirl(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
              role = data['girl']
              await self.remove_role(role=role, member=member)
              embed = discord.Embed(
                      description=f"{member.mention} Has Removed From girl",
                      color=0x01f5b6
              )
              await context.send(embed=embed)         

    @remove.command(
      name = "vip",
      description="remove vip role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to remove vip")
    async def rvip(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
              role = data['vip']
              await self.remove_role(role=role, member=member)
              embed = discord.Embed(
                      description=f"{member.mention} Has Removed From vip",
                      color=0x01f5b6
              )
              await context.send(embed=embed)  

    @remove.command(
      name = "guest",
      description="remove guest role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to remove guest")
    async def rguest(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
              role = data['guest']
              await self.remove_role(role=role, member=member)
              embed = discord.Embed(
                      description=f"{member.mention} Has Removed From guest",
                      color=0x01f5b6
              )
              await context.send(embed=embed) 

    @remove.command(
      name = "friend",
      description="remove friend role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to remove friend")
    async def rfriend(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
              role = data['frnd']
              await self.remove_role(role=role, member=member)
              embed = discord.Embed(
                      description=f"{member.mention} Has Removed From friend",
                      color=0x01f5b6
              )
              await context.send(embed=embed)        
          

    @remove.command(
      name = "clown",
      description="remove clown role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to remove clown")
    async def rclown(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
              role = data['clowns']
              await self.remove_role(role=role, member=member)
              embed = discord.Embed(
                      description=f"{member.mention} Has Removed From clown",
                      color=0x01f5b6
              )
              await context.send(embed=embed)   

    @remove.command(
      name = "artist",
      description="remove artist role",
    )
    @checks.not_blacklisted()
    @commands.has_permissions(administrator=True)
    @app_commands.describe(member="member to remove artist")
    async def rart(self, context: Context, member: discord.Member) -> None:
        if data := getConfig(context.guild.id):
              role = data['art']
              await self.remove_role(role=role, member=member)
              embed = discord.Embed(
                      description=f"{member.mention} Has Removed From artist",
                      color=0x01f5b6
              )
              await context.send(embed=embed)   

async def setup(bot):
    await bot.add_cog(Roles(bot))