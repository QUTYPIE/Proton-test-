import asyncio
import validators
import json as json_but_pain

from discord import Embed

MAIN_COLOR = 0x01f5b6
RED_COLOR = 0xFF0000

def success_embed(title, description):
    return Embed(
        title=title,
        description=description,
        color=MAIN_COLOR
    )


def meh_embed(title, description):
    return Embed(
        title=title,
        description=description
    )


def error_embed(title, description):
    return Embed(
        title=title,
        description=description,
        color=RED_COLOR
    )


async def edit_msg_multiple_times(ctx, time_, first_msg, other_msgs, final_emb):
    msg = await ctx.send(embed=Embed(title=first_msg, color=MAIN_COLOR))
    await asyncio.sleep(time_)

    for e in other_msgs:
        embed = Embed(title=e[0], color=MAIN_COLOR)
        if len(e) == 2:
            embed.description = e[1]
        await msg.edit(embed=embed)
        await asyncio.sleep(time_)

    await msg.edit(embed=final_emb)