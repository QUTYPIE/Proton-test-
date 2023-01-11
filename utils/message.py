import discord
import asyncio
from discord.ext import commands
from utils.embed import error_embed
from typing import Union

RED_COLOR = 0xFF0000

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
                    title=f"<:no:1040100153811533834> Cancelled!",
                    color=RED_COLOR
                )
            )
            return 'pain'
    except asyncio.TimeoutError:
        ctx.command.reset_cooldown(ctx)
        await msg_to_edit.edit(
            content="",
            embed=error_embed(
                f"<:no:1040100153811533834> Too late!",
                "You didn't answer in time! Please re-run the command."
            )
        )
        return 'pain'
    return msg
