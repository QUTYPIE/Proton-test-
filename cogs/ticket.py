import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio

def clean_code(content):
    if content.startswith('```') and content.endswith('```'):
        return "\n".join(content.split("\n")[1:][:-3])
    else:
        return content
      

class Pag():
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass
class close(Button):
    def __init__(self):
        super().__init__(label=f'Close', style=discord.ButtonStyle.success, custom_id="close")
        self.callback = self.button_callback
    
    async def button_callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Closing this ticketing in 5 seconds.', ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()

class closeTicket(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(close())

class create(Button):
    def __init__(self):
        super().__init__(label='Create ticket', style=discord.ButtonStyle.primary, custom_id=f'create')
        self.callback = self.button_callback
    
    async def button_callback(self, interaction: discord.Interaction):
        categ = discord.utils.get(interaction.guild.categories, name='Ticket-category')
        
        for ch in categ.channels:
            if ch.topic == str(interaction.user):
                await interaction.response.send_message("You already have a ticket open.", ephemeral=True)
                return
        overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.user: discord.PermissionOverwrite(read_messages=True),
                }
        channel = await categ.create_text_channel(f"ticket-{interaction.user.name}", overwrites=overwrites, topic=f'{interaction.user}')
        await interaction.response.send_message(f">>> Your ticket has been created at {channel.mention}", ephemeral=True)
        embed = discord.Embed(
                    title=f'Ticket',
                    description=f'Thanks for reaching out!\nThe supporters will be here shortly\nPlease be patient.',
                    color = 0x2f3136
      )

        await channel.send(f'{interaction.user.mention} Welcome', embed=embed, view=closeTicket())

class createTicket(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(create())

class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    def help_custom(self):
        emoji = '<:ticket:1040653004904333402>'
        label = "Ticket"
        description = "Shows Ticket Commands"
        return emoji, label, description


    @commands.group()
    @commands.has_permissions(manage_guild=True)
    async def ticket(self, ctx: commands.Context):
        embed = discord.Embed(title='Ticket', description="Create Below The Button To Create Ticket").set_thumbnail(url=self.bot.user.avatar)
        guild = ctx.guild
        await guild.create_category_channel(name="Ticket-category")
        await ctx.send(embed=embed, view=createTicket())


async def setup(bot):
    await bot.add_cog(TicketCog(bot))