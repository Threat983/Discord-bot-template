import os
import discord
from replit import db
from discord.ext import commands

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')



intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

#commands
@bot.event
async def on_ready():
  print(f"Logged in as {bot.user}")
@bot.command()
async def user(ctx):
  playername = ctx.author.name
  await ctx.send(playername)
@bot.tree.command(name="help" , description="Shows all commands")
async def help(interaction: discord.Interaction):
  await interaction.response.send_message("**Commands**\n!user - Shows your username\n!help - Shows all commands \n!balance -shows your balance")

bot.run('DISCORD_TOKEN')