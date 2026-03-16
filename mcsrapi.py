import discord as dc
from discord.ext import commands as cmd
import requests as req
import urllib

api = "https://api.mcsrranked.com/"

class MCSRRankedAPI: 
    def __init__(self):
        self.api = api
    def get_user_info(self, user): 
        user1 = urllib.parse.quote(user, safe='_')
        url = f"{self.api}users/{user1}"
        response = req.get(url, timeout=5)
        return response.json()
    def get_leaderboard(self): 
        response = req.get(f"{self.api}leaderboard", timeout=5)
        return response.json()
    def get_record_leaderboard(self): 
        response = req.get(f"{self.api}record-leaderboard", timeout=5)
        return response.json()
    def get_matchup(self, user1, user2):
        response = req.get(f"{self.api}users/{user1}/versus/{user2}", timeout = 5)
        return response.json()
