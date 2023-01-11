import discord
from discord.ext import commands
import random
import asyncio

class figt(commands.Cog):
  def __init__(self,bot):
    self.bot = bot


  def help_custom(self):
      emoji = '<:41:1027543537962717184>'
      label = "Combat"
      description = "Shows Combat Command"
      return emoji, label, description 

      
  @commands.hybrid_command()
  async def fight(self, ctx,member:discord.Member=None):

    if member == None:
      await ctx.reply(embed=discord.Embed(description='Mention A User'))

    else:
        def check(m):
          return m.author == ctx.author

        def check1(m):
          return m.author == member

        await ctx.reply(embed=discord.Embed(description="Name Your Character"))
        try:
          player1 = await self.bot.wait_for('message',check=check,timeout=30.0)

          

        except asyncio.TimeoutError:

          return await ctx.reply('Timeout : 30s')
        
        await ctx.reply(embed=discord.Embed(description=f"{member.mention} Name Your Character"))

        try:

          player2 = await self.bot.wait_for('message',check=check1,timeout=30.0)

        except asyncio.TimeoutError:

          return await ctx.send(f'{member.mention} Timeout : 30s')
        player1 = player1.content
        player2 = player2.content
        embed=discord.Embed(title=f'Welcome {player1} and {player2}',description='These are the Weapons and their uses',colour=discord.Colour.blue())
        embed.add_field(name="Axe",value='`Axes are heavy on attack, and have high possibility of disabling the enemy weapon`')
        embed.add_field(name='Sword',value="`Swords do medium attack, have medium attack speed, and medium defense`")
        embed.add_field(name='Spear',value="`Spears do heavy attack, at a fast speed, but r bad on defense`")
        embed.add_field(name='Dagger',value="`Daggers do less damage, but have the fastest attack speed in the game`")
        embed.add_field(name='Hammer',value="`Hammers have less chance of hitting but if they hit they do the most damage in the game`")
        embed.add_field(name='Club',value='`Clubs have the highest defense, in the game`')
        embed.add_field(name='Trident',value="`Tridents never miss and they do good damage and have good defense`")
        await ctx.send(embed=embed)
        await ctx.reply(embed=discord.Embed(description=f'What do you want to choose? {player1}'))
        player1_weapon = await self.bot.wait_for('message',check=check)
        await ctx.reply(embed=discord.Embed(description=f'What do you want to choose? {player2}'))
        player2_weapon = await self.bot.wait_for('message',check=check1)
        player1_weapon = player1_weapon.content
        player2_weapon=player2_weapon.content
        #player1 stats
        lives1 = 200 
        damage1 = 0
        defense1 = 0
        
        #player2 stats
        lives2 = 200
        damage2 = 0
        defense2 = 0
        #player1 weapon stats
        if player1_weapon.lower() == "sword":
            maxdamage1 = 25
            maxdefense1 = 30
            maxdisable_chance1 = 11
            maxchance1 = 20
        elif player1_weapon.lower() == "spear":
            maxdamage1 = 40
            maxdefense1 = 10
            maxdisable_chance1 = 11
            maxchance1 = 25
        elif player1_weapon.lower() == "axe":
            maxdamage1 = 35
            maxdefense1 = 20
            maxdisable_chance1 = 14
            maxchance1 = 15
        elif player1_weapon.lower() == "club":
            maxdamage1 = 20
            maxdefense1 = 60
            maxdisable_chance1 = 11
            maxchance1 = 15
        elif player1_weapon.lower() == "daggers" or player2_weapon.lower() == 'dagger':
            maxdamage1 = 15
            maxdefense1 = 20
            maxdisable_chance1 = 11
            maxchance1 = 40
        elif player1_weapon.lower() == "hammer":
            maxdamage1 = 80
            maxdefense1 = 15
            maxdisable_chance1 = 11
            maxchance1 = 20
        elif player1_weapon.lower() == "trident":
            maxdamage1 =  30
            maxdefense1 = 20
            maxdisable_chance1 = 11
            maxchance1 = 30
        else:
            await ctx.send('Game over due to wrong weapon choosing')
            return     #player2 weapon stats
        if player2_weapon.lower() == "sword":
            maxdamage2 = 25
            maxdefense2 = 30
            maxdisable_chance2 = 11
            maxchance2 = 20
        elif player2_weapon.lower() == "spear":
            maxdamage2 = 40
            maxdefense2 = 10
            maxdisable_chance2 = 11
            maxchance2 = 25
        elif player2_weapon.lower() == "axe":
            maxdamage2 = 35
            maxdefense2 = 20
            maxdisable_chance2 = 14
            maxchance2 = 15
            
        elif player2_weapon.lower() == "club":
            maxdamage2 = 20
            maxdefense2 = 60
            maxdisable_chance2 = 11
            maxchance2 = 15
        elif player2_weapon.lower() == "daggers" or player2_weapon.lower() == 'dagger':
            maxdamage2 = 15
            maxdefense2 = 20
            maxdisable_chance2 = 11
            maxchance2 = 40
        elif player2_weapon.lower() == "hammer":
            maxdamage2 = 80
            maxdefense2 = 15
            maxdisable_chance2 = 11
            maxchance2 = 20
        elif player2_weapon.lower() == "trident":
            maxdamage2 =  30
            maxdefense2 = 20
            maxdisable_chance2 = 11
            maxchance2 = 20
        else:
            await ctx.send(embed=discord.Embed(description='Game over due to wrong weapon choosing'))
            return
            
        while lives1 > 0 and lives2 > 0:
            player1_chance = random.randint(0,int(maxchance1))
            player2_chance = random.randint(0,int(maxchance2))
            if player1_chance >= player2_chance:
                await ctx.send(embed=discord.Embed(description=f"Since {player1} is faster than {player2}, its {player1}'s chance"))
                await ctx.reply(embed=discord.Embed(description="Attack or Defend?"))
                attack = await self.bot.wait_for('message',check=check)
                attack = attack.content
                if attack.lower() == "attack":
                    damage_delt = random.randint(5,int(maxdamage1))
                    if damage_delt > 10:
                        damage1 += damage_delt
                        damage1 -= defense2
                        lives2 -= damage1
                        damage1 = 0
                        defense2=0
                        await ctx.reply(embed=discord.Embed(description=f"You hit {player2} and dealt {damage_delt} damage\n{player2} has {lives2} health left!"))
                    else:
                        print(f"{player1} delt no damage")
                elif attack.lower() == "defend":
                    defense1 += random.randint(10, int(maxdefense1))
                    await ctx.send(embed=discord.Embed(description=f'Your defense now is {defense1}'))

                else:
                  await ctx.send(embed=discord.Embed(description='Invalid Option \n your Chance got Skipped'))

                while lives1 > 0 and lives2 > 0:
                  await ctx.send(embed=discord.Embed(description=f"Attack or Defend {player2}"))
                  attack = await self.bot.wait_for('message',check=check1)
                  attack = attack.content
                  if attack.lower() == "attack":
                      damage_delt = random.randint(5,int(maxdamage2))
                      if damage_delt > 10:
                          damage2 += damage_delt
                          damage2 -= defense1
                          lives1 -= damage2
                          damage2 = 0
                          defense1=0
                          await ctx.reply(embed=discord.Embed(description=f"You hit {player1} and dealt {damage_delt} damage\n{player1} has {lives1} health left!"))
                          if random.randint(0, int(maxdisable_chance1)) >= 10:
                              print("You have been disabled!")
                              player1_weapon = None
                              await ctx.send(embed=discord.Embed(description=f'{player1} Weapon Disabled \n {player2} Won With {lives2} Health'))
                              lives1=0
                              break
                              return
                            
                            
                              
                      else:
                          await ctx.send(embed=discord.Embed(description=f"{player2} Delt No Damage"))

                  elif attack.lower() == "defend":
                      defense1 += random.randint(10, int(maxdefense1))
                      print(f'Your defense now is {defense1}')

                  else:
                    await ctx.send(embed=discord.Embed(description='Invalid Option \n Chance Got Skipped'))

                  await ctx.send(embed=discord.Embed(description=f"Attack or Defend? {player1}"))
                  attack = await self.bot.wait_for('message',check=check)
                  attack = attack.content
                  if attack.lower() == "attack":
                      damage_delt = random.randint(5,int(maxdamage1))
                      if damage_delt > 10:
                          damage1 += damage_delt
                          damage1 -= defense2
                          lives2 -= damage1
                          damage1 = 0
                          defense2 = 0
                          await ctx.reply(embed=discord.Embed(description=f"You Beat {player2} And Gave {damage_delt} Damage\n{player2} Has {lives2} Health"))
                          if random.randint(0, int(maxdisable_chance2)) >= 10:
                              await ctx.send(embed=discord.Embed(description=f"{player1} Trashed {player2}  As Reason Is He Disabled {player2}'s Weapon"))
                              player2_weapon = None
                              lives2 = 0
                              break
            
                              return
                              
                      else:
                          await ctx.send(embed=discord.Embed(description=f"{player1} Got No Damage"))
                          
                  elif attack.lower() == "defend":
                      defense1 += random.randint(10, int(maxdefense1))
                      await ctx.send(embed=discord.Embed(description=f'Your Defense Is {defense1}'))

                  else:
                    await ctx.send(embed=discord.Embed(description='Invalid Option \n Chance Got Skipped'))

            elif player2_chance > player1_chance:
                await ctx.send(f'{player1} Your Opponent Is faster \n {player2}s Chance') 
                await ctx.reply(embed=discord.Embed(description="Attack or Defend"))
                attack = await self.bot.wait_for('message',check=check1)
                attack = attack.content
                if attack.lower() == "attack":
                    damage_delt = random.randint(5,int(maxdamage2))
                    if damage_delt > 10:
                        damage2 += damage_delt
                        damage2 -= defense1
                        lives1 -= damage2
                        defense1 = 0
                        damage2 = 0
                        await ctx.send(f"{player1} Got Hit And Got {damage_delt} Damage\n{player1} Has {lives1} Health")
                        # if random.randint(0, int(maxdisable_chance1)) >= 10:
                        #     await ctx.send("you have been disabled")
                        #     player2_weapon = None
                    else:
                        print(f"{player2} delt no damage")
                elif attack.lower() == "defend":
                    defense1 += random.randint(10, int(maxdefense2))
                    await ctx.send(embed=discord.Embed(description=f'{defense2} Is Your Defense'))

                else:
                  await ctx.send(embed=discord.Embed(description='Invalid Option \n Chance Got Skipped'))

                while lives1 > 0 and lives2 > 0:
                  await ctx.send(embed=discord.Embed(description=f"Attack or Defend? {player1}"))
                  attack = await self.bot.wait_for('message',check=check)
                  attack = attack.content
                  if attack.lower() == "attack":
                      damage_delt = random.randint(5,int(maxdamage1))
                      if damage_delt > 10:
                          damage1 += damage_delt
                          damage1 -= defense2
                          lives2 -= damage1
                          defense2 = 0
                          damage1 = 0
                          await ctx.send(f"You hit {player2} and dealt {damage_delt} damage\n{player2} has {lives2} health left")
                          if random.randint(0, int(maxdisable_chance1)) >= 10:
                              print("you have been disabled")
                              player2_weapon = None
                              await ctx.send(f'Weapon of {player2} is disabled!!! {player1} wins badly with {lives2} health left')
                              lives2 = 0
                              break
                              return
                              
                      else:
                          await ctx.send(f"{player2} Got No Damage")

                  elif attack.lower() == "defend":
                      defense1 += random.randint(10, int(maxdefense1))
                      print(f'Your defense now is {defense1}')

                  else:
                    await ctx.send('Invalid Option \n Chance Got Skipped')

                  await ctx.send(f"Attack or Defend? {player2}")
                  attack = await self.client.wait_for('message',check=check1)
                  attack = attack.content
                  if attack.lower() == "attack":
                      damage_delt = random.randint(5,int(maxdamage2))
                      if damage_delt > 10:
                          damage2 += damage_delt
                          damage2 -= defense1
                          defense1 = 0
                          lives1 -= damage2
                          damage2 = 0
                          await ctx.send(f"You hit {player1} and dealt {damage_delt} damage\n{player1} has {lives1} health left")
                          if random.randint(0, int(maxdisable_chance2)) >= 10:
                              await ctx.send(f'{player2} absolutely trashed {player1} with {lives2} health remaining because he disbaled {player1}s weapon!!!')
                              player1_weapon = None
                              lives1 = 0
                              break
                              return

                             
                              
          
                      else:
                          await ctx.send(f"{player2} Got No Damage")
                          
                  elif attack.lower() == "defend":
                      defense1 += random.randint(10, int(maxdefense2))
                      await ctx.send(f'{defense2} Is Your Defense')

                  else:
                    await ctx.send('Invalid Option \n Chance Got Skipped')

            if lives1 == 0:
              await ctx.send(embed=discord.Embed(description=f'{member.mention} Crushed {player1}{ctx.author.mention} With {lives2} Health'))

            else:
              await ctx.send(f'{player1}({ctx.author.mention}) absolutely crushed {player2}({member.mention}) with {lives1} health remaining!')

async def setup(bot):
  await bot.add_cog(figt(bot))