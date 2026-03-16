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
bot = cmd.Bot(command_prefix="!", intents=intents)

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

#For testing purposes to clear channel, will be removed in the future
@bot.command()
async def purge(ctx, limit: int):
    await ctx.channel.purge(limit=limit)

#BOT COMMANDS
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


@bot.command()
async def season(ctx):
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_leaderboard()
    season = data['data']['season']['number']
    seasonstart = datetime.fromtimestamp(data['data']['season']['startsAt']).strftime('%Y-%m-%d')
    seasonend = datetime.fromtimestamp(data['data']['season']['endsAt']).strftime('%Y-%m-%d')
    msg = (
        "```"
        f"Welcome to Season {season}!\n"
        f"Season Start: {seasonstart}\n"
        f"Season End: {seasonend}\n"
        f"Good luck to everyone playing this season! "
        "```"
    )
    await ctx.send(msg)


@bot.command()
async def leaderboard(ctx, limit: int = 20):
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_leaderboard()
    
    season = data['data']['season']['number']
    players = data['data']['users'][:limit] 
    msg = ( 
        "```"
        f"Displaying top {limit} players for season {season}\n"
        
    )
    for i in range(limit):
        player = players[i]
        elo = player['eloRate']
        tier = elo_tier(elo)
        msg += (
            f"{i+1}. {player['nickname']} - {tier} ({elo})\n"
        )
    msg += "```"
    await ctx.send(msg)


@bot.command()
#Add an option to filter for a user or seedtype in the future 
async def recordbest(ctx, limit: int = 10):
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_record_leaderboard()
    runs = data['data'][:limit]

    msg = (
        "```"
        f"Displaying All-time Best Runs\n"
    )
    for i in range(limit):
        time_ms = runs[i]['time']
        seconds = (time_ms // 1000) % 60
        minutes = (time_ms // 1000) // 60
        msg += (
            f"{i+1}: {runs[i]['user']['nickname']} - {minutes}:{seconds:02d}\n"
            f"Season: {runs[i]['season']} - ({datetime.fromtimestamp(runs[i]['date']).strftime('%Y-%m-%d')})\n"
            f"Seed Type: {runs[i]['seed']['overworld']}\n"
            f"Bastion: {runs[i]['seed']['nether']}\n"
            f"-----------------------------\n"
            
        )
    msg += "```"
    await ctx.send(msg)


@bot.command()
async def matchup(ctx, user1: str , user2: str):
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_matchup(user1, user2)
    player_data = data['data']['players']
    matchup_results = data['data']['results']
    elo_change = data['data']['changes']
    player1_ID = player_data[0]['uuid']
    player2_ID = player_data[1]['uuid']
    player1 = player_data[0]['nickname']
    player2 = player_data[1]['nickname']
    p1_elo = player_data[0]['eloRate']
    p2_elo = player_data[1]['eloRate']
    


    msg = (
        "```"
        f"Displaying most recent match between {user1} vs {user2}\n"
        f"#{player_data[0]['eloRank']} : {player1} ({player_data[0]['country'].upper()}) - {elo_tier(p1_elo)} {player_data[0]['eloRate']}\n"
        f"#{player_data[1]['eloRank']} : {player2} ({player_data[1]['country'].upper()}) - {elo_tier(p2_elo)} {player_data[1]['eloRate']}\n"
        f"- - - - - - - - - - - - - - - - - - - - - - - \n"
        f"RESULTS: \n"
        f"Ranked: {matchup_results['ranked']['total']} matches \n"
        f"        {player1} : {matchup_results['ranked'][player1_ID]} wins\n"
        f"        {player2} : {matchup_results['ranked'][player2_ID]} wins\n"
        f"Casual: {matchup_results['casual']['total']} matches \n"
        f"        {player1} : {matchup_results['casual'][player1_ID]} wins \n"
        f"        {player2} : {matchup_results['casual'][player2_ID]} wins \n"
        f"Total Elo Change: \n"
        f"- {player1} {elo_change[player1_ID]:+}\n"
        f"- {player2} {elo_change[player2_ID]:+}\n"
        "```"
    )
    await ctx.send(msg)



  
bot.run(token, log_handler=handler, log_level=logging.DEBUG)