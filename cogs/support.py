from __future__ import annotations

import asyncio
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
import discord
import copy
from typing import Optional, List, Dict, Any, Union


class FeedbackModal(discord.ui.Modal, title='Submit Feedback'):
    summary = discord.ui.TextInput(label='Summary', placeholder='A brief explanation of what you want')
    details = discord.ui.TextInput(label='Details', style=discord.TextStyle.long, required=False)

    def __init__(self, cog: Support) -> None:
        super().__init__()
        self.cog: Support = cog

    async def on_submit(self, interaction: discord.Interaction) -> None:
        channel = self.cog.feedback_channel
        if channel is None:
            await interaction.response.send_message('Could not submit your feedback, sorry about this', ephemeral=True)
            return

        embed = self.cog.get_feedback_embed(interaction, summary=str(self.summary), details=self.details.value)
        await channel.send(embed=embed)
        await interaction.response.send_message('Successfully submitted feedback', ephemeral=True)


class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @property
    def feedback_channel(self) -> discord.TextChannel:
        guild = self.bot.get_guild(1029604436953276447)
        if guild is None:
            return None

        return guild.get_channel(1034353367310413874)


    def get_feedback_embed(
        self,
        obj: Context | discord.Interaction,
        *,
        summary: str,
        details: str = None,
    ) -> discord.Embed:
        e = discord.Embed(title='Feedback', colour=0x2F3136)

        if details is not None:
            e.description = details
            e.title = summary[:256]
        else:
            e.description = summary

        if obj.guild is not None:
            e.add_field(name='Server', value=f'{obj.guild.name} (ID: {obj.guild.id})', inline=False)

        if obj.channel is not None:
            e.add_field(name='Channel', value=f'{obj.channel} (ID: {obj.channel.id})', inline=False)

        if isinstance(obj, discord.Interaction):
            e.timestamp = obj.created_at
            user = obj.user
        else:
            e.timestamp = obj.message.created_at
            user = obj.author

        e.set_author(name=str(user), icon_url=user.display_avatar.url)
        e.set_footer(text=f'Author ID: {user.id}')
        return e

    @commands.command()
    @commands.cooldown(rate=1, per=60.0, type=commands.BucketType.user)
    async def feedback(self, ctx: Context, *, content: str):
        """Gives feedback about the bot.
        This is a quick way to request features or bug fixes
        without being in the bot's server.
        The bot will communicate with you via PM about the status
        of your request if possible.
        You can only request feedback once a minute.
        """

        channel = self.feedback_channel
        if channel is None:
            return

        e = self.get_feedback_embed(ctx, summary=content)
        await channel.send(embed=e)
        await ctx.send(f'Successfully sent feedback')

    @app_commands.command(name='feedback')
    async def feedback_slash(self, interaction: discord.Interaction):
        """Give feedback about the bot directly to the owner."""

        await interaction.response.send_modal(FeedbackModal(self))  


    @commands.command(hidden=True)
    @commands.is_owner()
    async def sudo(
        self,
        ctx: Context,
        channel: Optional[discord.TextChannel],
        who: Union[discord.Member, discord.User],
        *,
        command: str,
    ):
        """Run a command as another user optionally in another channel."""
        msg = copy.copy(ctx.message)
        new_channel = channel or ctx.channel
        msg.channel = new_channel
        msg.author = who
        msg.content = ctx.prefix + command
        new_ctx = await self.bot.get_context(msg, cls=type(ctx))
        await self.bot.invoke(new_ctx)      

async def setup(bot):
    await bot.add_cog(Support(bot))      