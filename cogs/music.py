import discord
import wavelink
from discord import app_commands
from wavelink.ext import spotify
from discord.ext import commands
import logging
from typing import Any, Dict, Union, Optional
from discord.enums import try_enum
import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
import json
import datetime
import discord
import psutil
import platform
import aiohttp
import datetime as dt
import datetime
import random
import typing as t
import requests
import re
from discord.ext.commands.errors import CheckFailure
import asyncio
import os
from wavelink import Player
import async_timeout
import discord
from youtubesearchpython import VideosSearch


LYRICS_URL = "https://some-random-api.ml/lyrics?title="
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"


class NotConnectedToVoice(CheckFailure):
    """User not connected to any voice channel"""

    pass


class PlayerNotConnected(CheckFailure):
    """Player not connected"""

    pass


class MustBeSameChannel(CheckFailure):
    """Player and user not in same channel"""

    pass


class NothingIsPlaying(CheckFailure):
    """Nothing is playing"""

    pass


class NotEnoughSong(CheckFailure):
    """Not enough songs in queue"""

    pass


class InvalidLoopMode(CheckFailure):
    """Invalid loop mode"""

    pass
class DisPlayer(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.queue = asyncio.Queue()
        self.bound_channel = None
        self.track_provider = "yt"

    async def destroy(self) -> None:
        self.queue = None

        await super().stop()
        await super().disconnect()

    async def do_next(self) -> None:
        if self.is_playing():
            return

        timeout = int(os.getenv("DISMUSIC_TIMEOUT", 300))

        try:
            with async_timeout.timeout(timeout):
                track = await self.queue.get()
        except asyncio.TimeoutError:
            if not self.is_playing():
                await self.destroy()

            return

        self._source = track
        await self.play(track)
        self.client.dispatch("dismusic_track_start", self, track)
        await self.invoke_player()


    async def invoke_player(self, ctx: commands.Context = None) -> None:
        track = self.source

        if not track:
            raise NothingIsPlaying("Player is not playing anything.")

        embed = discord.Embed(
            title=track.title, url=track.uri, color=0x01f5b6
        )
        embed.set_author(
            name=track.author,
            url=track.uri,
            icon_url=self.client.user.display_avatar.url,
        )
        try:
            embed.set_thumbnail(url=track.thumb)
        except AttributeError:
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/776345413132877854/940540758442795028/unknown.png"
            )
        embed.add_field(
            name="Length",
            value=f"{int(track.length // 60)}:{int(track.length % 60)}",
        )
        embed.add_field(name="Looping", value=self.loop)
        embed.add_field(name="Volume", value=self.volume)

        next_song = ""

        if self.loop == "CURRENT":
            next_song = self.source.title
        else:
            if len(self.queue._queue) > 0:
                next_song = self.queue._queue[0].title

        if next_song:
            embed.add_field(name="Next Song", value=next_song, inline=False)

        if not ctx:
            return await self.bound_channel.send(embed=embed)

        await ctx.send(embed=embed)
class Check:

    async def userInVoiceChannel(self, ctx, bot):
        """Check if the user is in a voice channel"""
        if ctx.author.voice:
            return True
        await ctx.channel.send(f"{bot.emojiList.false} {ctx.author.mention} You are not connected in a voice channel!")
        return False
        
    
    async def botInVoiceChannel(self, ctx, bot):
        """Check if the bot is in a voice channel"""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)


        if player.is_connected:
            return True
        await ctx.channel.send(f"{bot.emojiList.false} {ctx.author.mention} I'm not connected in a voice channel!")
        return False

    async def botNotInVoiceChannel(self, ctx, bot):
        """Check if the bot is not in a voice channel"""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if not player.is_connected:
            return True
        await ctx.channel.send(f"{bot.emojiList.false} {ctx.author.mention} I'm already connected in a voice channel!")
        return False
        

    async def userAndBotInSameVoiceChannel(self, ctx, bot):
        """Check if the user and the bot are in the same voice channel"""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if (
            (bot.user.id in ctx.author.voice.channel.voice_states) and
            (ctx.author.id in ctx.author.voice.channel.voice_states)
        ):
            return True
        await ctx.channel.send(f"{bot.emojiList.false} {ctx.author.mention} You are not connected in the same voice channel that the bot!")
        return False
    
    async def botIsPlaying(self, ctx, bot):
        """Check if the bot is playing"""
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player.is_playing:
            return True
        await ctx.channel.send(f"{bot.emojiList.false} {ctx.author.mention} There is currently no song to replay!")
        return False
__all__ = (
    "WavelinkError",
    "AuthorizationFailure",
    "LavalinkException",
    "LoadTrackError",
    "BuildTrackError",
    "NodeOccupied",
    "InvalidIDProvided",
    "ZeroConnectedNodes",
    "NoMatchingNode",
    "QueueException",
    "QueueFull",
    "QueueEmpty",
)


class WavelinkError(Exception):
    """Base WaveLink Exception"""
class InvalidEqPreset(commands.CommandError):
    pass

class AuthorizationFailure(WavelinkError):
    """Exception raised when an invalid password is provided toa node."""


class LavalinkException(WavelinkError):
    """Exception raised when an error occurs talking to Lavalink."""


class LoadTrackError(LavalinkException):
    """Exception raised when an error occurred when loading a track."""

class NoLyricsFound(commands.CommandError):
    pass
class NoMoreTracks(commands.CommandError):
    pass

class BuildTrackError(LavalinkException):
    """Exception raised when a track is failed to be decoded and re-built."""

    def __init__(self, data):
        super().__init__(data["error"])


class NodeOccupied(WavelinkError):
    """Exception raised when node identifiers conflict."""

class InvalidTimeString(commands.CommandError):
    pass
class InvalidIDProvided(WavelinkError):
    """Exception raised when an invalid ID is passed somewhere in Wavelink."""


class ZeroConnectedNodes(WavelinkError):
    """Exception raised when an operation is attempted with nodes, when there are None connected."""

class InvalidRepeatMode(commands.CommandError):
    pass
  
class NoMatchingNode(WavelinkError):
    """Exception raised when a Node is attempted to be retrieved with a incorrect identifier."""
class QueueIsEmpty(commands.CommandError):
    """AtLeast Have  Queue"""

class QueueException(WavelinkError):
    """Base WaveLink Queue exception."""

    pass


class QueueFull(QueueException):
    """Exception raised when attempting to add to a full Queue."""

    pass


class QueueEmpty(QueueException):
    """Exception raised when attempting to retrieve from an empty Queue."""

    pass
VoiceChannel = Union[
    discord.VoiceChannel, discord.StageChannel
]  

logger: logging.Logger = logging.getLogger(__name__)
class TrackNotFound(commands.CommandError):
    """Не найдена песня"""
    pass




class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Play / Pause", style=discord.ButtonStyle.blurple, emoji="<:pause_play_button:1039776501677183006>")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)
        
        if player.is_paused():
            await player.resume()
            mbed1 = discord.Embed(title="Proton | Music", description="Now Playing", color=0x01f5b6)
            return await interaction.response.send_message(embed=mbed1, ephemeral=True)
        elif player.is_playing():
            await player.pause()
            mbed = discord.Embed(title="Proton | Music", description="Successfully Paused The Music", color=0x01f5b6)
            return await interaction.response.send_message(embed=mbed, ephemeral=True)
        elif player is None:
            return await interaction.response.send_message(embed=discord.Embed(title="Proton | Music", description="Not Connected To Voice Channel", ephemeral=True))
        else:
            return await interaction.response.send_message(embed=discord.Embed(title="Proton | Music", description="No Music Currently Playing", ephemeral=True))

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.success, emoji="<:stop:1039776585571635200>", row=0)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            return await interaction.response.send_message(embed=discord.Embed(title="Proton | Music", description="Not Connected To Voice Channel", ephemeral=True))
        
        if player.is_playing:
            player.queue.clear()
            await player.stop()
            mbed = discord.Embed(title="Proton | Music", description="Successfully Stopped Music", color=0x01f5b6)
            return await interaction.response.send_message(embed=mbed, ephemeral=True)
        else:
            return await interaction.response.send_message(embed=discord.Embed(title="Proton | Music", description="No music currently playing", ephemeral=True))

    @discord.ui.button(label="Leave", style=discord.ButtonStyle.danger, emoji="<:leave:1039776301692768308>", row=0)
    async def dc_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        node = wavelink.NodePool.get_node()
        player = node.get_player(interaction.guild)

        if player is None:
            return await interaction.response.send_message(embed=discord.Embed(title="Proton | Music", description="Not Connected To Voice Channel", ephemeral=True))
    
        await player.disconnect()
        mbed = discord.Embed(title="Proton | Music", description="Successfully Left vc", color=0x01f5b6)
        await interaction.response.send_message(embed=mbed,  ephemeral=True)



    @discord.ui.button(label="Invite", style=discord.ButtonStyle.blurple, emoji="<:role:1030068644908126238>")
    async def confirukfmgujm(self, interaction: discord.Interaction, button: discord.ui.Button):
            mbed1 = discord.Embed(title="Proton | Invite", description="[Click To Invite Me](https://discord.com/api/oauth2/authorize?client_id=1027428088562319391&permissions=8&scope=bot%20applications.commands)", color=0x01f5b6)
            return await interaction.response.send_message(embed=mbed1, ephemeral=True)
class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot  
        self.playlist = []
        self.user_timer = {}
        self.user_all_time = {}


      
    def help_custom(self):
        emoji = '<a:music:1040652431941443604>'
        label = "Music"
        description = "Shows Music Comamnds"
        return emoji, label, description     
    
    async def create_nodes(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host="lavalink-replit-2.tomatotomato3.repl.co", port="443", https=True ,password="sorrows",region="asia", spotify_client=spotify.SpotifyClient(client_id="d52f6a05b7ac4ea1b953eadbd2b6ba45", client_secret="e43ff5d74bcd4eb28e55e5976b7b282e"))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Cog is now ready!")
        await self.bot.loop.create_task(self.create_nodes())

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node <{node.identifier}> is now Ready!")



    @commands.hybrid_group(name="play",with_app_command = True, description="play youtube music", aliases=[("p")])
    @app_commands.describe(search="Search word or URL (spotify or youtube)")    
    async def play(self, ctx: commands.Context, *, search:str):
        await ctx.defer()

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            embed=discord.Embed(title="Proton | Music", description=f"<a:xD_tick:1041515205965926461> | Successfully Connected To {ctx.author.voice.channel.mention} ", color=0x01f5b6)
            await ctx.send(embed=embed)
        else:
            vc: wavelink.Player = ctx.voice_client
            vc.chanctx = ctx.channel

        if 'https://open.spotify.com' in str(search):

            if vc.queue.is_empty and not vc.is_playing():

                track = await spotify.SpotifyTrack.search(query=search, return_first=True)

                await vc.play(track)

                mbed = discord.Embed(title="<a:playing:1041778100465307648> Now Playing", color=0x01f5b6)
                mbed.add_field(name="<:title:1041777765906645002> Title", value=track.title)
                mbed.add_field(name="<:duration:1041777813960798258> Duration Time", value=round(track.duration / 60, 2))
                
                mbed.add_field(name="<:song:1041777872907550860> Song Author", value=track.author) 
                mbed.set_image(url="https://storage.googleapis.com/spotifynewsroom-jp.appspot.com/1/2020/12/Spotify_Logo_CMYK_Green.png")
                mbed.set_footer(text="Made with 💖 By Proton Developement")


                view = Buttons() 
                await ctx.send(embed=mbed, view=view)

            else:
                track = await spotify.SpotifyTrack.search(query=search, return_first=True)
                await vc.queue.put_wait(track)
                await ctx.send(embed=discord.Embed(title="Proton | Music", description=f'`{track}` Added To The Queue'))

        elif 'https://www.youtube.com/' in str(search):

            if vc.queue.is_empty and not vc.is_playing():

                track1 = await vc.node.get_tracks(query=search, cls=wavelink.Track)

                await vc.play(track1[0])
                mbed = discord.Embed(title="<a:playing:1041778100465307648> Now Playing", color=0x01f5b6)
                mbed.add_field(name="Song Url", value=search)
                mbed.add_field(name="<:title:1041777765906645002> Title", value=track1)
                 
                mbed.set_image(url="https://wavelink.readthedocs.io/en/1.0/_static/logo.png")



                view = Buttons() 
                await ctx.send(embed=mbed, view=view)


            else:
                track1 = await vc.node.get_tracks(query=search, cls=wavelink.Track)
                await vc.queue.put_wait(track1[0])
                await ctx.reply(embed=discord.Embed(title="Proton | Music", description=f'`{track1}` Added To The Queue'))

        else:

            if vc.queue.is_empty and not vc.is_playing(): 

                track2 = await wavelink.YouTubeTrack.search(query=search, return_first=True)

                await vc.play(track2)

                mbed = discord.Embed(title="Playing", color=0x01f5b6)
                mbed.add_field(name="<:title:1041777765906645002> Title", value=track2.title)
                mbed.add_field(name="<:duration:1041777813960798258> Duration", value=round(track2.duration / 60, 2))
                
                mbed.add_field(name="<:song:1041777872907550860> Song Author", value=track2.author) 
                mbed.set_image(url=track2.thumb)


                view = Buttons() 
                await ctx.send(embed=mbed, view=view)

            else:

                track2 = await wavelink.YouTubeTrack.search(query=search, return_first=True)
                await vc.queue.put_wait(track2)
                await ctx.send(embed=discord.Embed(title="Proton | Music", description=f'`{track2}` Added To The Queue'))

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track , reason):

        if not player.queue.is_empty:
            ctx = player.chanctx
            new_song = player.queue.get()
            await player.play(new_song)



            if hasattr(new_song, 'thumb'):
                mbed = discord.Embed(title="<a:playing:1041778100465307648> Now Playing", color=0x01f5b6)
                mbed.add_field(name="<:title:1041777765906645002> Title", value=new_song.title)
                mbed.add_field(name="<:duration:1041777813960798258> Duration", value=round(new_song.duration / 60, 2))

                mbed.add_field(name="<:song:1041777872907550860> Song Author", value=new_song.author) 
                mbed.set_image(url=new_song.thumb) 
                view = Buttons() 
                await ctx.send(embed=mbed, view=view)

            else:
                mbed = discord.Embed(title="<a:playing:1041778100465307648> Now Playing", color=0x01f5b6)
                mbed.add_field(name="<:title:1041777765906645002> Title", value=new_song.title)
                mbed.add_field(name="<:duration:1041777813960798258> Duration", value=round(new_song.duration / 60, 2))
                mbed.add_field(name="<:song:1041777872907550860> Song Author", value=new_song.author) 
                mbed.set_image(url="https://wavelink.readthedocs.io/en/1.0/_static/logo.png") 
                view = Buttons() 
                await ctx.send(embed=mbed, view=view)

    @commands.hybrid_group(name="disconnect", description="Leave voice channel", with_app_command=True, aliases=[("dc")])   
    async def leave_command(self, ctx:commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if ctx.author.voice is None:
            return await ctx.reply(embed=discord.Embed(title="Proton | Music", description="Not Connected To Voice Channel"))
        
        await player.disconnect()
        mbed = discord.Embed(title="Proton | Music", description=f"Successfully Left {ctx.author.voice.channel.mention} Vc", color=0x01f5b6)
 
        await ctx.send(embed=mbed)

    @commands.hybrid_group(name="stop", description="Stop", with_app_command=True)    
    async def stop_command(self, ctx:commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        
        if ctx.author.voice is None:
            return await ctx.reply(embed=discord.Embed(title="Proton | Music", description="Not Connected To Voice Channel"))
        
        if player.is_playing:
            player.queue.clear()
            await player.stop()
            mbed = discord.Embed(title="Successfully Stopped Song", color=0x01f5b6)
            view = Buttons() 
            await ctx.send(embed=mbed, view=view)
        else:
            return await ctx.reply(embed=discord.Embed(title="Proton | Music", description="No Music Recently Playing"))

    @commands.hybrid_group(name="skip", description="Skip", with_app_command=True, aliases=[("s")])    
    async def skip_command(self, ctx:commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        
        if ctx.author.voice is None:
            return await ctx.reply(embed=discord.Embed(title="Proton | Music", description="Not Connected To Voice Channel"))
            
        if player.is_playing:
            await player.stop()
            mbed = discord.Embed(title="Proton | Music", description="Successfully Skipped The Song", color=0x01f5b6)

            await ctx.send(embed=mbed)
        else:
            return await ctx.reply(embed=discord.Embed(title="Proton | Music", description="no Music Recently Playing"))

  
    @commands.hybrid_group(name="pause", description="Pause", with_app_command=True)    
    async def pause_command(self, ctx:commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if ctx.author.voice is None:
            return await ctx.reply(embed=discord.Embed(title="Proton | Music", description="Not Connected To Voice Channel"))
            
        if not player.is_paused():
            if player.is_playing():
                await player.pause()
                mbed = discord.Embed(title="Paused", color=0x01f5b6)
                view = Buttons() 
                await ctx.send(embed=mbed, view=view)
            else:
                return await ctx.reply(embed=discord.Embed(title="Proton | Music", description="No Music Playing"))
        else:
            return await ctx.reply(embed=discord.Embed(title="Proton | Music", description="Song Already Paused"))


    @commands.hybrid_group(name="resume", description="Resume", with_app_command=True)    
    async def resume_command(self, ctx:commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if ctx.author.voice is None:
            return await ctx.reply(embed=discord.Embed(title="Proton | Music", description="Not Connected To Voice Channel"))
            
        if player.is_paused():
            await player.resume()
            mbed = discord.Embed(title="Resumed", color=0x01f5b6)
            view = Buttons() 
            await ctx.send(embed=mbed, view=view)
        else:
            return await ctx.reply(embed=discord.Embed(title="Proton | Music", description="Song Already Resumed"))

    @commands.hybrid_group(name="queue", description="Check queue", with_app_command=True, aliases=[("q")])
    async def queue_command(self, ctx):
      if not ctx.voice_client:
        return await ctx.reply(embed=discord.Embed(title="Proton | Music", description=f"{ctx.message.author.mention} Not Connected In Voice"))
      elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send(embed=discord.Embed(title="Proton | Music", description=f"{ctx.message.author.mention} Need To Join Vc"))
      else:
        vc: wavelink.Player = ctx.voice_client

      if vc.queue.is_empty:
        return await ctx.send(embed=discord.Embed(title="Proton | Music", description="Queue is empty!"))

      em = discord.Embed(color=0x01f5b6, title="Queue")
      copy = vc.queue.copy()
      count = 0
      for song in copy:
        count += 1
        em.add_field(name=f"Position {count}", value=f"`{song.title}`")

      return await ctx.send(embed=em)  

    @commands.hybrid_group(name="bassboost", description="Boost bass", with_app_command=True, aliases=[("bb")])
    async def boost_command(self, ctx:commands.Context):

        """Bass Boost Filter """
        vc: wavelink.Player = ctx.voice_client

        if vc is None:
            return await ctx.reply(embed=discord.Embed(title="Proton | Music", description="Not Connected To Voice Channel"))
        bands = [(0, 0.2), (1, 0.15), (2, 0.1), (3, 0.05), (4, 0.0),(5, -0.05), (6, -0.1), (7, -0.1), (8, -0.1), (9, -0.1), (10, -0.1), (11, -0.1), (12, -0.1), (13, -0.1), (14, - 0.1)]
        await vc.set_filter(wavelink.Filter(equalizer=wavelink.Equalizer(name="MyOwnFilter",bands=bands)), seek=True)
        await ctx.reply(embed=discord.Embed(title="Proton | Music", description="Bass Boost Enabled"))


    @commands.hybrid_group(name="removeboost", description="Remove boost", with_app_command=True, aliases=[("rbb")])
    async def rmvboost_command(self, ctx:commands.Context):
        vc: wavelink.Player = ctx.voice_client
        await vc.set_filter(wavelink.Filter(equalizer=wavelink.Equalizer.flat()),seek=True)
        await ctx.reply(embed=discord.Embed(title="Proton | Music", description="Bass Boost Disabled"))
      
    @commands.hybrid_command(name="kodane", description="Reward......", with_app_command=True)
    async def kodane(self, ctx:commands.Context):
        search = "It's a reward. I'll give you my materials [GB materials]"
        track = await wavelink.YouTubeTrack.search(query=search, return_first=True)

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client
            
        await vc.play(track)
        await ctx.reply(embed=discord.Embed(title="Proton | Music", description="As a reward, give me my offspring."))
        await ctx.reply("https://pbs.twimg.com/media/FK_tTvmaAAAYzMp.jpg")


    @commands.hybrid_command(name="move", description="Reward......", with_app_command=True)
    async def move_to(self, ctx, channel: discord.VoiceChannel) -> None:
        """Moves Bot With Vc Id
        """
        await ctx.guild.change_voice_state(channel=channel)
        logger.info(f"Moving to voice channel:: {channel.id}")




    @commands.hybrid_group(name = "volume",
                    usage="<0 to 500>",
                    description = "Change the bot's volume.", aliases=[("v")])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def volume(self, ctx, volume):

        if not await Check().userInVoiceChannel(ctx, self.bot): return 
        if not await Check().botInVoiceChannel(ctx, self.bot): return 
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 

        if (
            (not volume.isdigit()) or 
            (int(volume)) < 0 or 
            (int(volume) > 500)
        ):
            return await ctx.send(embed=discord.Embed(title="Proton | Music", description=f" {ctx.author.mention} Volume Must Be 0 To 500"))
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        volume = int(volume)
        await player.set_volume(volume)

        embed=discord.Embed(title="Proton | Music", description=f"<a:xD_tick:1041515205965926461> | Successfully Changed Volume To : `{volume}%`", color=0x01f5b6)
        await ctx.send(embed=embed)


 

    @commands.hybrid_group(description="Songs Queue")
    async def playing(self, ctx):
      if not ctx.voice_client:
        return await ctx.send(embed=discord.Embed(title="Proton | Music", description=f"{ctx.message.author.mention} Not Connected In A Voice Channel") )  
      elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send(f"{ctx.message.author.mention} Need To Join Vc")
      else:
        vc: wavelink.Player = ctx.voice_client
    
      if not vc.is_playing():
        return await ctx.send(embed=discord.Embed(title="Proton | Music", description="Nothing is playing"))

      em = discord.Embed(title="Now playing", description=f"{vc.track}")
      em.add_field(name="Artist", value=f"`{vc.track.author}`")   
      em.add_field(name="Duration", value=f"`{datetime.timedelta(seconds=vc.track.length)}`")
      return await ctx.send(embed=em)


    @commands.hybrid_group(description="Shuffle Queue")
    async def shuffle(self, ctx):
      if not ctx.voice_client:
        return await ctx.send(embed=discord.Embed(title="Proton | Music", description=f"{ctx.message.author.mention} Not Connected In Voice"))   
      elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.reply(embed=discord.Embed(title="Proton | Music", description=f"{ctx.message.author.mention} Need To Join Vc"))
      else:
        vc: wavelink.Player = ctx.voice_client

      copy = vc.queue.copy()
      random.shuffle(copy)
      vc.queue = copy
      await ctx.send(embed=discord.Embed(title="Proton | Music", description=f"{ctx.message.author.mention} Shuffled The Queue"))


    @commands.hybrid_group(description="Pulls Queue")
    async def pull(self, ctx, index: int):
      if not ctx.voice_client:
        return await ctx.reply(embed=discord.Embed(title="Proton | Music", description=f" {ctx.message.author.mention} Not Connected In Voice"))
      elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send(embed=discord.Embed(title="Proton | Music", description=f"{ctx.message.author.mention} Need To Join Vc"))
      else:
        vc: wavelink.Player = ctx.voice_client

      if index > len(vc.queue) or index < 1:
        return await ctx.reply(embed=discord.Embed(title="Proton | Music", description=f"Must Be Between 1 And {len(vc.queue)}"))

      removed = vc.queue.pop(index - 1)

      await ctx.send(embed=discord.Embed(title="Proton | Music", description=f"{ctx.message.author.mention} Pulls Out `{removed.title}` From Queue"))

    @commands.hybrid_group(description="Clears Queue")
    async def qclear(self, ctx):
      if not ctx.voice_client:
        return await ctx.reply(embed=discord.Embed(title="Proton | Music", description=f" {ctx.message.author.mention} Not Connected In Voice"))
      elif not getattr(ctx.author.voice, "channel", None):
        return await ctx.send(embed=discord.Embed(title="Proton | Music", description=f"{ctx.message.author.mention} Need To Join Vc"))
      else:
        vc: wavelink.Player = ctx.voice_client

      await vc.queue.clear()
      return await ctx.send(embed=discord.Embed(title="Proton | Music", description=f"{ctx.message.author.mention} Clears The Queue"))


    @commands.hybrid_group(name="lyrics", aliases=["lr"])
    async def lyrics_command(self, ctx, *, name: t.Optional[str]):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        name = name or player.queue.current_track.title

        async with ctx.typing():
            async with aiohttp.request("GET", LYRICS_URL + name, headers={}) as r:
                if not 200 <= r.status <= 299:
                    raise NoLyricsFound

                data = await r.json()

                if len(data["lyrics"]) > 2000:
                    return await ctx.reply(f"<{data['links']['genius']}>")

                embed = discord.Embed(
                    title=data["title"],
                    description=data["lyrics"],
                    colour=0x01f5b6,
                    timestamp=dt.datetime.utcnow()
                )
                embed.set_thumbnail(url=data["thumbnail"]["genius"])
                embed.set_author(name=data["author"])
                await ctx.reply(embed = embed)



    @commands.hybrid_group(name="seek", aliases=["sk"])
    async def seek_command(self, ctx, position: str):
        """'seek [minute]m[second]'"""
        node = wavelink.NodePool.get_node()
        player: Player = node.get_player(ctx.guild)
       # if player.queue.is_empty:
          #  raise QueueIsEmpty

        if not (match := re.match(TIME_REGEX, position)):
            raise InvalidTimeString

        if match.group(3):
            secs = (int(match.group(1)) * 60) + (int(match.group(3)))
        else:
            secs = int(match.group(1))

        await player.seek(secs * 1000)
        await ctx.reply(embed=discord.Embed(title="Proton | Music", description="Successfully Seeks Music"))


async def setup(bot):
    await bot.add_cog(Music(bot))