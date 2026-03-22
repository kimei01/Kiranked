import discord as dc
from datetime import datetime
from dotenv import load_dotenv
import requests as req
from discord.ext import commands as cmd
from discord import app_commands
from utils.calculatorUtils import  format_time, format_playtime, elo_tier
from utils.embeds_utils import get_embed_color, get_country_flag, get_rank_icon, get_skin
import mcsrapi

def rankedPlayer(user): 
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_user_info(user)
    season_num = api.get_current_season()
    leaderboard_url = api.get_official_leaderboard(user)
    user_info = data['data']

    nickname = user_info['nickname']
    uuid = user_info['uuid']
    country = user_info['country']  or ('N/A').upper()

    #Get user Elo
    elo = user_info['eloRate']
    elo_rank = user_info['eloRank']
    elo_highest = user_info['seasonResult']['highest']
    elo_lowest = user_info['seasonResult']['lowest']
    tier = elo_tier(elo)

    #Get Season Statistics 
    statistics_season = user_info['statistics']['season']
    season_bestTime = format_time(statistics_season['bestTime']['ranked'])
    season_playtime= format_playtime(statistics_season['playtime']['ranked'])
    season_bestWinstreak = statistics_season['highestWinStreak']['ranked']
    season_matches = statistics_season['playedMatches']['ranked']
    season_wins = statistics_season['wins']['ranked']
    season_forfeit = statistics_season['forfeits']['ranked']
    season_completions = statistics_season['completions']['ranked']
    season_winrate = round(season_wins/season_matches * 100, 2) 
    season_forfeitrate = round(season_forfeit/season_matches * 100, 2)

    #Get All-time Statistics 
    statistics_total = user_info['statistics']['total']
    total_bestTime = format_time(statistics_total['bestTime']['ranked'])
    total_playtime = format_playtime(statistics_total['playtime']['ranked'])
    total_bestWinstreak = statistics_total['highestWinStreak']['ranked']
    total_matches = statistics_total['playedMatches']['ranked']
    total_wins = statistics_total['wins']['ranked']
    total_forfeit = statistics_total['forfeits']['ranked']
    total_completions = statistics_total['completions']['ranked']
    total_winrate = round(total_wins/total_matches * 100, 2)
    total_forfeitrate = round(total_forfeit/total_matches * 100, 2)
        

    join_date = datetime.fromtimestamp(user_info['timestamp']['firstOnline']).strftime('%Y-%m-%d')
    last_online = datetime.fromtimestamp(user_info['timestamp']['lastOnline']).strftime('%Y-%m-%d')
    #Check if current user elo is their HIGHEST
    if elo == elo_highest: 

        title_msg = (
            f" #{elo_rank}  {get_country_flag(country)} **{nickname}** \n"
            f"{get_rank_icon(tier)}**{tier}** ({elo}) <:peak:1484255430753390593> PEAK ELO" 
    )
    else: 
        title_msg = (
            f" #{elo_rank}  {get_country_flag(country)} **{nickname}** \n"
            f"{get_rank_icon(tier)}**{tier}** ({elo})"
        )
    separator = "━━━━━━━━━━━━━━━━━━━━"
    embed = dc.Embed(title = title_msg, description = f"[{nickname}]({leaderboard_url}) has a played {season_matches} matches in season {season_num} and achieved the highest elo of **{elo_highest}** and a lowest of **{elo_lowest}** \n", color = get_embed_color(tier) )
    embed.set_thumbnail(url=get_skin(uuid))
    embed.add_field(name = f"Season {season_num} statistics", value =  f"{separator}\n \u2023 Matches Played: **{season_matches}** \n (*{season_completions} completions*)\n \u2023 Winrate: **{season_winrate}%** (*{season_wins} Wins*) \n \u2023 Forfeit Rate: **{season_forfeitrate}%** \n \u2023 Best Time: **{season_bestTime}** \n \u2023 Playtime: **{season_playtime} Hrs** \n", inline = True)
    embed.add_field(name = f"All Time Statistics", value = f"{separator}\n\u2023 Matches Played: **{total_matches}** \n (*{total_completions} completions*) \n \u2023 Winrate: **{total_winrate}%** (*{total_wins} Wins*)\n \u2023 Forfeit Rate: **{total_forfeitrate}%** \n \u2023 Best Time: **{total_bestTime}** \n \u2023 Playtime: **{total_playtime} Hrs** \n", inline = True)
    embed.set_footer(text = f"Joined: {join_date} / Last Online {last_online}")
    return embed

def show_season(): 
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_leaderboard()
    season = data['data']['season']
    season_num = season['number']
    season_start = datetime.fromtimestamp(season['startsAt'])
    season_end = datetime.fromtimestamp(season['endsAt'])
    time_now = datetime.now()
    days_since_start = (time_now - season_start).days
    days_until_end = (season_end - time_now).days
    embed = dc.Embed(title = f"Welcome To Season {season_num}!", description = f" \u2023 The Season started on {season_start.strftime('%A, %B %d %Y')}\n (**{days_since_start}** days ago..) \n \u2023 The Season will end on {season_end.strftime('%A, %B %d %Y')} \n (**{days_until_end}** from now..)", color = 3426654)
    embed.set_thumbnail(url = "https://yt3.googleusercontent.com/cAIIfKHjVsBjDrnhHtnFm3r_2azfrgo7HurdMX_hLiZSs4E8INfvde3FCwab5uf3f06ZYzq5=s900-c-k-c0x00ffffff-no-rj")
    embed.set_footer(text = "Good luck to everyone playing this season!")
    return embed

def leaderboard_player(limit: int): 
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_leaderboard()

    season = data['data']['season'] 
    season_num = season['number']
    season_start = datetime.fromtimestamp(season['startsAt'])
    season_end = datetime.fromtimestamp(season['endsAt'])
    time_now = datetime.now()
    days_since_start = (time_now - season_start).days
    days_until_end = (season_end - time_now).days
    user_info = data['data']['users'][:limit] 

    msg = (
        "```"
        
        
    )
    for i in range(limit):
        user = user_info[i]
        elo = user['eloRate']
        tier = elo_tier(elo)
        msg += (
            f"{str(i+1).rjust(2)}. {user['nickname'].ljust(20)}  {tier} ({elo})\n"
        )
    msg += "```"
    
    embed = dc.Embed(                        
        title=f"Season {season_num} Leaderboard",
        description=f"Season {season_num} started **{days_since_start}** days ago and will end in **{days_until_end}** days",
        color = 15277667		
    )
    embed.add_field(name=f"Displaying top {limit} players for season {season_num}\n", value=msg, inline=False)  
    return embed


def leaderboard_bestTime(limit: int):
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



            f"Season: {runs[i]['season']} on ({datetime.fromtimestamp(runs[i]['date']).strftime('%Y-%m-%d')})\n"
            f"Seed Type: {runs[i]['seed']['overworld']}\n"
            f"Bastion: {runs[i]['seed']['nether']}\n"
            f"-----------------------------\n"
            
        )
    msg += "```"
    embed = dc.Embed(title = f"All-Time Fastest Runs", description = f"", color = 2899536)
    embed.add_field(name=f"Showing Top {limit} Fastest Runs", value = msg, inline=False)
    return embed

def playerVersus(user1, user2): 
    api = mcsrapi.MCSRRankedAPI()
    data = api.get_matchup(user1, user2)
    player_data = sorted(data['data']['players'], key=lambda x: x['eloRank'])
    matchup_results = data['data']['results']

    #User1 Statistics 
    p1_ID = player_data[0]['uuid']
    p1_nickname = player_data[0]['nickname']
    p1_elo = player_data[0]['eloRate']
    p1_eloRank = player_data[0]['eloRank']
    p1_tier = elo_tier(p1_elo)
    p1_country = player_data[0]['country']
    p1_rankedWins = matchup_results['ranked'][p1_ID]
    
    #User 2 Statistics
    p2_ID = player_data[1]['uuid']
    p2_nickname = player_data[1]['nickname']
    p2_elo = player_data[1]['eloRate']
    p2_tier = elo_tier(p2_elo)
    p2_eloRank = player_data[1]['eloRank']
    p2_country = player_data[1]['country']
    p2_rankedWins = matchup_results['ranked'][p2_ID]

    elo_change = data['data']['changes']
    p1_elochange = elo_change[p1_ID]
    p2_elochange = elo_change[p2_ID]


    embed = dc.Embed(title = f"Displaying head-to-head record \n {user1} vs {user2}", description ="", color = 2067276)
    embed.add_field (name = f"#{p1_eloRank}  {get_country_flag(p1_country)} **{p1_nickname}** {get_rank_icon(p1_tier)}**{p1_tier}** ({p1_elo})",value = "", inline = False)
    embed.set_thumbnail (url = "https://yt3.googleusercontent.com/cAIIfKHjVsBjDrnhHtnFm3r_2azfrgo7HurdMX_hLiZSs4E8INfvde3FCwab5uf3f06ZYzq5=s900-c-k-c0x00ffffff-no-rj")
    embed.add_field (name = f"#{p2_eloRank}  {get_country_flag(p2_country)} **{p2_nickname}** {get_rank_icon(p2_tier)}**{p2_tier}** ({p2_elo})",value = "", inline = False)
    embed.add_field (name = f"Ranked Matches", value = f"\u2023 {p1_nickname}: **{p1_rankedWins} Wins** \n \u2023 {p2_nickname}: **{p2_rankedWins} Wins**\n", inline = True)
    embed.add_field (name = f"Total Elo Gain/Loss", value = f"\u2023 {p1_nickname}: **{p1_elochange:+}** \n \u2023 {p2_nickname}: **{p2_elochange:+}**", inline = True)
    return embed