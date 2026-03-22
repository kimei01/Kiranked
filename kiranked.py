import discord as dc
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
import requests as req
from discord.ext import commands as cmd
from discord import app_commands
from embeds import rankedPlayer, leaderboard_bestTime, leaderboard_player, show_season, playerVersus

import mcsrapi

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = dc.Intents.all()
bot = cmd.Bot(command_prefix="!", intents=intents)

#Remove GuildId to sync bot globally / Replace GuildID with YOUR private serverID for testing
guild_id = dc.Object(id=1480616258507505714)

@bot.event
async def on_ready():
    print(f"{bot.user} is online with no issues")
    try: 
        guild = dc.Object(1480616258507505714) #Remove or Replace with your Guildid
        synced = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced)} commands to guild {guild}")
    except Exception as e: 
        print(f"Error syncing commands {e}")

    
#For testing purposes to clear channel, will be removed in the future
@bot.command()
async def purge(ctx, limit: int):
    await ctx.channel.purge(limit=limit)

#BOT COMMANDS
@bot.tree.command(name = "ranked", description = f"Look up statistics of a ranked player", guild=guild_id)
@app_commands.describe(user="The player's username")
async def ranked(interaction: dc.Interaction, user: str):
    try:
        await interaction.response.defer()
        await interaction.followup.send(embed=rankedPlayer(user))
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")
        


@bot.tree.command(name = "season", description = f"Shows the current season", guild= guild_id)
async def season(interaction: dc.Interaction):
    try:
        await interaction.response.defer()
        await interaction.followup.send(embed=show_season())
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")
    

@bot.tree.command(name = "leaderboard", description = f"shows the top players", guild = guild_id)
async def leaderboard(interaction: dc.Interaction, limit: int = 20):
    try:
        await interaction.response.defer()
        await interaction.followup.send(embed=leaderboard_player(limit))
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")


@bot.tree.command(name = "leaderboard_runs", description = f"Shows the top fastest runs", guild = guild_id )
#Add an option to filter for a user or seedtype in the future 
async def recordbest(interaction: dc.Interaction, limit: int = 5):
    try:
        await interaction.response.defer()
        await interaction.followup.send(embed=leaderboard_bestTime(limit))
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")


@bot.tree.command(name = "versus", description = "Shows the most recent match between 2 players", guild = guild_id)
async def matchup(interaction: dc.Interaction, user1: str , user2: str):
    try:
        await interaction.response.defer()
        await interaction.followup.send(embed=playerVersus(user1, user2))
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")
    
    

    


    


  
bot.run(token, log_handler=handler, log_level=logging.DEBUG)