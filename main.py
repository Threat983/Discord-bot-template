import os
import discord
from discord.ext import commands
import random
#basic currency system bot
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True
intents.moderation = True
bot = commands.Bot(command_prefix='!', intents=intents)

class player:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def save_balance(self, balance):
        self.balance = balance
        with open(f"{self.name}.txt", "w") as file:
            file.write(str(balance))

    def load_balance(self):
        with open(f"{self.name}.txt", "r") as file:
            return int(file.read())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def user(ctx):
    username = ctx.author.name
    player_instance = player(username, balance=0)
    try:
        balance = player_instance.load_balance()
        player_instance.balance = balance
        await ctx.send(f"Welcome back, {username}! Your balance is {balance}.")
    except FileNotFoundError:
        await ctx.send(f"New player created: {username} with balance 0.")
        player_instance.save_balance(0)

@bot.command()
async def coinflip(ctx, amount: int):
    username = ctx.author.name
    player_instance = player(username, balance=0)
    try:
        balance = player_instance.load_balance()
        player_instance.balance = balance
    except FileNotFoundError:
        balance = 0
        player_instance.save_balance(balance)

    if player_instance.balance >= amount:
        def random_coinflip():
            return random.choice(["heads", "tails"])
        result = random_coinflip()
        if result == "heads":
            new_balance = balance + amount
            await ctx.send(f"🎲 Result: {result}\nYou won! New balance: {new_balance}")
            player_instance.save_balance(new_balance)
        else:
            new_balance = balance - amount
            await ctx.send(f"🎲 Result: {result}\nYou lost! New balance: {new_balance}")
            player_instance.save_balance(new_balance)
    else:
        await ctx.send(f"You don't have enough money. Your balance: {balance}")


@bot.tree.command(name="help", description="Shows all commands")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message("**Commands**\n!user - Shows your username\n!help - Shows all commands \n!balance - shows your balance")

bot.run('DISCORD_TOKEN')
