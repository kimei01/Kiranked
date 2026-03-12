import discord as dc
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
import requests as req
from discord.ext import commands as cmd

import mcsrapi

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = dc.Intents.all()
bot = cmd.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online with no issues")



def elo_tier(elo):
    if elo >= 2000:
        return "Netherite"
    elif elo >= 1800:
        return "Diamond III"
    elif elo >= 1650:
        return "Diamond II"
    elif elo >= 1500:
        return "Diamond I"
    elif elo >= 1400:
        return "Emerald III"
    elif elo >= 1300:
        return "Emerald II"
    elif elo >= 1200:
        return "Emerald I"
    elif elo >= 1100:
        return "Gold III"
    elif elo >= 1000:
        return "Gold II"
    elif elo >= 900:
        return "Gold I"
    elif elo >= 800:
        return "Iron III"
    elif elo >= 700:
        return "Iron II"
    elif elo >= 600:
        return "Iron I"
    elif elo >= 500:
        return "Coal III"
    elif elo >= 400:
        return "Coal II"
    elif elo >= 0:
        return "Coal I"
    else:
        return "Unrated"


@bot.command()
async def ranked(ctx, *, user: str): 

    user = user.strip()
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_user_info(user)
    user_info = data['data']

    elo = data['data']['eloRate']
    tier = elo_tier(elo)
    if '_' in user:
        user = user.replace('_', '\\_')  
    msg = (
        f"Displaying ranked info for {user}\n"
        f"```"
        f"Username: {data['data']['nickname']}\n"
        f"Country: {(data['data']['country'] or ('N/A')).upper()}\n"
        f"Current Standing: {data['data']['eloRank']}\n"
        f"{tier} : ({elo}) "
        f"(Season High: {data['data']['seasonResult']['highest']}/Season Low: {data['data']['seasonResult']['lowest']})\n"
        f"Joined: {datetime.fromtimestamp(data['data']['timestamp']['firstOnline']).strftime('%Y-%m-%d')}\n"
        f"Last Online: {datetime.fromtimestamp(data['data']['timestamp']['lastOnline']).strftime('%Y-%m-%d')}\n"
        f"```" 
        ) 
    
        

    await ctx.send(msg)

    
   

    

bot.run(token, log_handler=handler, log_level=logging.DEBUG)