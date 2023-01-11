import discord
from discord.ext import commands,tasks
import akinator as ak
import random
import requests
import json
import asyncio
import itertools
import asyncio
import discord
from typing import Optional, Union, List
from discord.ext import commands
from discord import SelectOption
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from helpers import checks, db_manager
import discord
import asyncio
from discord.ext import commands
from typing import Union
import random
from helpers import checks
import aiohttp
import discord
from collections import defaultdict
suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = (
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Jack",
    "Queen",
    "King",
    "Ace",
)
values = {
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": 11,
}

playing = True


class Choice(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Heads", style=discord.ButtonStyle.blurple)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "heads"
        self.stop()

    @discord.ui.button(label="Tails", style=discord.ButtonStyle.blurple)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = "tails"
        self.stop()


class RockPaperScissors(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Scissors", description="You choose scissors.", emoji="✂"
            ),
            discord.SelectOption(
                label="Rock", description="You choose rock.", emoji="🪨"
            ),
            discord.SelectOption(
                label="paper", description="You choose paper.", emoji="🧻"
            ),
        ]
        super().__init__(
            placeholder="Choose Your Option",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        choices = {
            "rock": 0,
            "paper": 1,
            "scissors": 2,
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]

        bot_choice = random.choice(list(choices.keys()))
        bot_choice_index = choices[bot_choice]

        result_embed = discord.Embed(color=0x01f5b6)
        result_embed.set_author(
            name=interaction.user.name,
            icon_url=interaction.user.avatar.url
        )

        if user_choice_index == bot_choice_index:
            result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x01f5b6
        elif user_choice_index == 0 and bot_choice_index == 2:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x01f5b6
        elif user_choice_index == 1 and bot_choice_index == 0:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x01f5b6
        elif user_choice_index == 2 and bot_choice_index == 1:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x01f5b6
        else:
            result_embed.description = f"**I won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x01f5b6
        await interaction.response.edit_message(embed=result_embed, content=None, view=None)


class RockPaperScissorsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(RockPaperScissors())

      
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        # return self.rank + ' of ' + self.suit

        # self.rank + ' of ' + self.suit + ". value: " +
        return str(values[self.rank])


class Deck:
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(
                    Card(suit, rank)
                )  # build Card objects and add them to the list

    def __str__(self):
        deck_comp = ""  # start with an empty string
        for card in self.deck:
            deck_comp += "\n " + card.__str__()  # add each Card object's print string
        return "The deck has :" + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1  # add to self.aces

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    def __init__(self):
        self.total = (
            100  # This can be set to a default value or supplied by a user input
        )
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


# Functions
def take_bet():
    return "How many chips would you like to bet? "


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand, x):
    global playing  # to control an upcoming while loop

    while True:
        # input h or s

        if x[0].lower() == "h":
            hit(deck, hand)  # hit() function defined above

        elif x[0].lower() == "s":

            playing = False
            return "Player stands. Dealer is playing."

        else:
            continue
            # return "Sorry, please try again."

        break


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print("", dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep="\n ")


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep="\n ")
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep="\n ")
    print("Player's Hand =", player.value)


def player_busts(player, dealer, chips):
    print("Player busts!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("Dealer busts!")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print("Dealer wins!")
    chips.lose_bet()


def push(player, dealer):
    print("Dealer and Player tie! It's a push.")
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
                    title=f" Cancelled!",
                    color=0x01f5b6
                )
            )
            return 'pain'
    except asyncio.TimeoutError:
        ctx.command.reset_cooldown(ctx)
        await msg_to_edit.edit(
            content="",
            embed=discord.Embed(title=
                f" Too late!", description=
                "You didn't answer in time! Please re-run the command."
            )
        )
        return 'pain'
    return 
class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout: Optional[int] = None):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"This is {self.ctx.author.mention}'s command, not yours.", ephemeral=True)
            return False
        return True
class TruthAndDareView(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None

    @discord.ui.button(label="Dare", custom_id='dare', style=discord.ButtonStyle.danger)
    async def dare(self, button, interaction):
        self.value = 'dare'
        self.stop()

    @discord.ui.button(label="Truth", custom_id='truth', style=discord.ButtonStyle.green)
    async def truth(self, button, interaction):
        self.value = 'truth'
        self.stop()
      
class Akinator(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.round_number = 0
        self.last_to_leave_vc = defaultdict(lambda: None)
    def help_custom(self):
        emoji = '<:Games:1040655788538085376>'
        label = "Games"
        description = "Shows Game Commands"
        return emoji, label, description
  
    @commands.group(aliases=["aki"])
    async def akinator(self,ctx):
        intro=discord.Embed(title="Akinator",description="Hello, "+ctx.author.mention+"I am Akinator!!!",color=00000)
        intro.set_thumbnail(url="https://en.akinator.com/bundles/elokencesite/images/akinator.png?v93")
        intro.set_footer(text="I Will Guess Your Character")
        bye=discord.Embed(title="Akinator",description="Bye, "+ctx.author.mention,color=00000)
        bye.set_footer(text="Akinator left the chat!!")
        bye.set_thumbnail(url="https://i.pinimg.com/originals/28/fc/0b/28fc0b88d8ded3bb8f89cb23b3e9aa7b.png")
        await ctx.reply(embed=intro)
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y", "n","p","b","yes","no","probably","idk","back"]
        try:
            aki = ak.Akinator()
            q = aki.start_game()
            while aki.progression <= 80:
                question=discord.Embed(title="Question",description=q,color=00000)
                ques=["https://i.imgflip.com/uojn8.jpg","https://ih1.redbubble.net/image.297680471.0027/flat,750x1000,075,f.u1.jpg"]
                question.set_thumbnail(url=ques[random.randint(0,1)])
                question.set_footer(text="Your answer:(y/n/p/idk/b)")
                question_sent=await ctx.reply(embed=question)
                try:
                    msg = await self.bot.wait_for("message", check=check , timeout=30)
                except asyncio.TimeoutError:
                    await question_sent.delete()
                    await ctx.reply("Sorry you took too long to respond!(waited for 30sec)")
                    await ctx.reply(embed=bye)
                    return
                await question_sent.delete()
                if msg.content.lower() in ["b","back"]:
                    try:
                        q=aki.back()
                    except ak.CantGoBackAnyFurther:
                        await ctx.reply(e)
                        continue
                else:
                    try:
                        q = aki.answer(msg.content.lower())
                    except ak.InvalidAnswerError as e:
                        await ctx.reply(e)
                        continue
            aki.win()
            answer=discord.Embed(title=aki.first_guess['name'],description=aki.first_guess['description'],color=00000)
            answer.set_thumbnail(url=aki.first_guess['absolute_picture_path'])
            answer.set_image(url=aki.first_guess['absolute_picture_path'])
            answer.set_footer(text="Was I correct?(y/n)")
            await ctx.reply(embed=answer)
            #await ctx.reply(f"It's {aki.first_guess['name']} ({aki.first_guess['description']})! Was I correct?(y/n)\n{aki.first_guess['absolute_picture_path']}\n\t")
            try:
                correct = await self.bot.wait_for("message", check=check ,timeout=30)
            except asyncio.TimeoutError:
                await ctx.reply("Sorry you took too long to respond!(waited for 30sec)")
                await ctx.reply(embed=bye)
                return
            if correct.content.lower() == "y":
                yes=discord.Embed(title="Yeah!!!",color=00000)
                yes.set_thumbnail(url="https://i.pinimg.com/originals/ae/aa/d7/aeaad720bd3c42b095c9a6788ac2df9a.png")
                await ctx.reply(embed=yes)
            else:
                no=discord.Embed(title="Oh Noooooo!!!",color=00000)
                no.set_thumbnail(url="https://i.pinimg.com/originals/0a/8c/12/0a8c1218eeaadf5cfe90140e32558e64.png")
                await ctx.reply(embed=no)
            await ctx.reply(embed=bye)
        except Exception as e:
            await ctx.reply(e)




    @commands.hybrid_group(aliases=['tnd', 'dare', 'truth', 'tod'], help="Play truth and dare!")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def truthordare(self, ctx: commands.Context):
        view = TruthAndDareView(ctx)
        main_msg = await ctx.reply("Pick what u want to do?", view=view)
        await view.wait()
        if not view.value:
            return await main_msg.edit(content="Command cancelled or timed out!", view=None)
        if view.value == 'truth':
            truth_is_always_painful = random.choice([
                "When was the last time you lied?",
                "When was the last time you cried?",
                "What's your biggest fear?",
                "What's your biggest fantasy?",
                "Do you have any fetishes?",
                "What's something you're glad your mum doesn't know about you?",
                "Have you ever cheated on someone?",
                "What's the worst thing you've ever done?",
                "What's a secret you've never told anyone?",
                "Do you have a hidden talent?",
                "Who was your first celebrity crush?",
                "What are your thoughts on polyamory?",
                "What's the worst intimate experience you've ever had?",
                "Have you ever cheated in an exam?",
                "What's the most drunk you've ever been?",
                "Have you ever broken the law?",
                "What's the most embarrassing thing you've ever done?",
                "What's your biggest insecurity?",
                "What's the biggest mistake you've ever made?",
                "What's the most disgusting thing you've ever done?",
                "Who would you like to kiss in this room?",
                "What's the worst thing anyone's ever done to you?",
                "Have you ever had a run in with the law?",
                "What's your worst habit?",
                "What's the worst thing you've ever said to anyone?",
                "Have you ever peed in the shower?",
                "What's the strangest dream you've had?",
                "Have you ever been caught doing something you shouldn't have?",
                "What's the worst date you've been on?",
                "What's your biggest regret?",
                "What's the biggest misconception about you?",
                "Where's the weirdest place you've had sex?",
                "Why did your last relationship break down?",
                "Have you ever lied to get out of a bad date?",
                "What's the most trouble you've been in?"
            ])
            await main_msg.edit(content=f"```\n{truth_is_always_painful}\n```", view=None)
            msg_check = await wait_for_msg(ctx, 60, main_msg)
            if msg_check == 'pain':
                return
            else:
                await main_msg.edit(content="Oh, is that so? 😏 I didn't know that. **Shame! Shame!**", view=None)
        elif view.value == 'dare':
            dare_is_more_and_always_painful = random.choice([
                "Show the most embarrassing photo on your phone",
                "Show the last five people you texted and what the messages said",
                "Let the rest of the group DM someone from your Instagram account",
                "Eat a raw piece of garlic",
                "Do 100 squats",
                "Keep three ice cubes in your mouth until they melt",
                "Say something dirty to the person on your left",
                "Give a foot massage to the person on your right",
                "Put 10 different available liquids into a cup and drink it",
                "Yell out the first word that comes to your mind",
                "Give a lap dance to someone of your choice",
                "Remove four items of clothing",
                "Like the first 15 posts on your Facebook newsfeed",
                "Eat a spoonful of mustard",
                "Keep your eyes closed until it's your go again",
                "Send a sext to the last person in your phonebook",
                "Show off your orgasm face",
                "Seductively eat a banana",
                "Empty out your wallet/purse and show everyone what's inside",
                "Do your best sexy crawl",
                "Pretend to be the person to your right for 10 minutes",
                "Eat a snack without using your hands",
                "Say two honest things about everyone else in the group",
                "Twerk for a minute",
                "Try and make the group laugh as quickly as possible",
                "Try to put your whole fist in your mouth",
                "Tell everyone an embarrassing story about yourself",
                "Try to lick your elbow",
                "Post the oldest selfie on your phone on Instagram Stories",
                "Tell the saddest story you know",
                "Howl like a wolf for two minutes",
                "Dance without music for two minutes",
                "Pole dance with an imaginary pole",
                "Let someone else tickle you and try not to laugh",
                "Put as many snacks into your mouth at once as you can"
            ])
            await main_msg.edit(content=f"```\n{dare_is_more_and_always_painful}\n```", view=None)
            msg_check = await wait_for_msg(ctx, 60, main_msg)
            if msg_check == 'pain':
                return
            else:
                await main_msg.edit(content="Oh, seems like u have some guts. Well done.", view=None)

      
    @commands.hybrid_group()
    @app_commands.describe(description="Shows Blackjack Game")
    async def blackjack(self, ctx):
        while True:
            self.round_number += 1
            # Print an opening statement
            await ctx.channel.send(embed=discord.Embed(description=
                "Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
            Dealer hits until she reaches 17. Aces count as 1 or 11.\n", color=0x01f5b6
            ))

            # Create & shuffle the deck, deal two cards to each player
            deck = Deck()
            deck.shuffle()

            player_hand = Hand()
            player_hand.add_card(deck.deal())
            player_hand.add_card(deck.deal())

            dealer_hand = Hand()
            dealer_hand.add_card(deck.deal())
            dealer_hand.add_card(deck.deal())

            # Set up the Player's chips
            player_chips = Chips()  # remember the default value is 100

            # Prompt the Player for their bet
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            await ctx.channel.send(take_bet())
            try:
                msg = await self.bot.wait_for("message", timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await ctx.reply("Check Your Dm's")
                await ctx.author.send("Please answer within 30 seconds")
            else:
                if int(msg.content) > player_chips.total:
                    await ctx.reply("Sorry, your bet can't exceed", player_chips.total)
                else:
                    player_chips.bet = int(msg.content)

            # Show cards (but keep one dealer card hidden)
            embed = discord.Embed(
                title="Round {}".format(self.round_number), colour=0x01f5b6
            )

            dealer_cards = (
                " <card hidden>\n"
                + str(dealer_hand.cards[1])
                + "\nTotal: "
                + str(dealer_hand.cards[1])
            )
            embed.add_field(name="Dealer's Hand:", value=dealer_cards)

            player_cards = ""
            total = 0
            for x in player_hand.cards:
                player_cards += str(x) + "\n"
                total += int(str(x))
            player_cards += "Total: " + str(total)

            embed.add_field(name="Player's Hand:", value=player_cards)
            await ctx.send(embed=discord.Embed)

            first_time = True
            global playing
            while playing:  # recall this variable from our hit_or_stand function
                if not first_time:
                    self.round_number += 1
                first_time = False
                # Prompt for Player to Hit or Stand

                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel

                await ctx.channel.reply(embed=discord.Embed(description=
                    "Would you like to Hit or Stand? Enter 'h' or 's' "
                ))
                try:
                    msg = await self.bot.wait_for(
                        "message", timeout=30.0, check=check
                    )
                except asyncio.TimeoutError:
                    await ctx.reply(embed=discord.Embed(description="Check Your Dm's"))
                    await ctx.author.send(embed=discord.Embed(description="Please answer within 30 seconds"))
                else:
                    hit_or_stand(deck, player_hand, msg.content)

                # Show cards (but keep one dealer card hidden)
                embed = discord.Embed(
                    title="Round {}".format(self.round_number + 1),
                    colour=0x01f5b6,
                )

                dealer_cards = (
                    " <card hidden>\n"
                    + str(dealer_hand.cards[1])
                    + "\nTotal: "
                    + str(dealer_hand.cards[1])
                )
                embed.add_field(name="Dealer's Hand:", value=dealer_cards)

                player_cards = ""
                total = 0
                for x in player_hand.cards:
                    player_cards += str(x) + "\n"
                    total += int(str(x))
                player_cards += "Total: " + str(total)

                embed.add_field(name="Player's Hand:", value=player_cards)
                await ctx.send(embed=discord.Embed)

                # If player's hand exceeds 21, run player_busts() and break out of loop
                if player_hand.value > 21:
                    player_busts(player_hand, dealer_hand, player_chips)
                    break

                    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
            if player_hand.value <= 21:

                while dealer_hand.value < 17:
                    hit(deck, dealer_hand)

                    # Show all cards
                embed = discord.Embed(title="Round Ended", colour=0x01f5b6)

                dealer_cards = ""
                for i in dealer_hand.cards:
                    dealer_cards += str(i) + " "
                embed.add_field(name="Dealer's Hand:", value=dealer_cards)

                player_cards = ""
                total = 0
                for x in player_hand.cards:
                    player_cards += str(x) + " "
                    total += int(str(x))
                player_cards += "Total: " + str(total)
                embed.add_field(name="Player's Hand:", value=player_cards)
                await ctx.send(embed=discord.Embed)

                # Run different winning scenarios
                if dealer_hand.value > 21:
                    dealer_busts(player_hand, dealer_hand, player_chips)
                elif dealer_hand.value > player_hand.value:
                    dealer_wins(player_hand, dealer_hand, player_chips)
                elif dealer_hand.value < player_hand.value:
                    player_wins(player_hand, dealer_hand, player_chips)
                else:
                    push(player_hand, dealer_hand)
                    # Inform Player of their chips total

            await ctx.channel.reply(embed=discord.Embed(description=
                "\nPlayer's winnings stand at" + str(player_chips.total)
            ))

            # Ask to play again
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            await ctx.channel.reply(embed=discord.Embed(description=
                "Would you like to play another hand? Enter 'y' or 'n' "
            ))
            try:
                msg = await self.bot.wait_for("message", timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await ctx.reply(embed=discord.Embed(description="Please answer within 30 seconds"))
            else:
                if msg.content[0].lower() == "y":
                    playing = True
                    continue
                else:
                    print("Thanks for playing!")
                    break


    @commands.hybrid_command(
        name="rps",
        description="Play the rock paper scissors game against the bot."
    )
    @checks.not_blacklisted()
    async def rock_paper_scissors(self, context: Context) -> None:
        """
        Play the rock paper scissors game against the bot.
        """
        view = RockPaperScissorsView()
        await context.send("Please make your choice", view=view)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
      if after.channel or before.channel is None:
        return
      time = discord.utils.utcnow()
      self.last_to_leave_vc[before.channel.id] = {"member": member, "time": time.timestamp()}

      
    @commands.hybrid_command(name="last", help="Gets the last member to leave a voice channel.")
    @commands.guild_only()
    async def last_member(self, ctx , *, voice_channel: Optional[discord.VoiceChannel] = None):
      if voice_channel is None and ctx.author.voice is None:
        return await ctx.reply(embed=discord.Embed(title="You must either select a voice channel or be in one.", color=0x01f5b6))
      if voice_channel is None:
        voice_channel = ctx.author.voice.channel
      if not isinstance(voice_channel, discord.VoiceChannel):
        return await ctx.reply(embed=discord.Embed(title="That is not a voice channel.", color=0x01f5b6))
      member = self.last_to_leave_vc[voice_channel.id]
      if member is None:
        return await ctx.reply(embed=discord.Embed(title=f"No currently saved departing member of `{voice_channel}` saved.", description="I'll catch the next one :)", color=0x01f5b6))
      await ctx.reply(embed=discord.Embed(title=f"`{member['member']}` left `{voice_channel.mention}` <t:{int(member['time'])}:R> ago."))








      
async def setup(bot):
    await bot.add_cog(Akinator(bot))