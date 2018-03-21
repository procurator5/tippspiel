#!/usr/bin/env python
# coding=utf-8
from tippspiel.xmlsoccer import XmlSoccer

from tippspiel.models import League, Team, Match
from django.utils import timezone
import datetime
import bet.settings

class Loader_Xmlsoccer():
    def __init__(self, api_key, use_demo=True):
        self.loader = XmlSoccer(api_key, use_demo)
        
    def LoadLeagues(self):    
        leagues = self.loader.call_api(method='GetAllLeagues')
        for league in leagues:
            try:
                row = League(league_name = league['Name'], country = league['Country'], 
                             is_cup = self.strToBool(league['IsCup']))
                row.save()
            except KeyError:
                pass

    def LoadTeams(self):    
        teams = self.loader.call_api(method='GetAllTeams')
        for team in teams:
            try:
                row = Team(name = team['Name'], country = team['Country'], 
                            handle = team['Name'][:3].upper(),
                            stadium = team['Stadium'])
                row.save()
            except KeyError:
                pass

    def LoadMatches(self):
        # I define current date/time (startDateString) and current date +2 mouths (endDateString)
        startDateString = timezone.now().isoformat()
        endDateString = (timezone.now() + datetime.timedelta(days=58)).isoformat()   
        matches = self.loader.call_api(method='GetFixturesByDateInterval', startDateString=startDateString, endDateString=endDateString)
        for match in matches:
            try:
                try:
                    row = Match.objects.get(xmlsoccer_matchid=match['Id'])
                except Match.DoesNotExist:
                    row = Match()
                row.date = match['Date']
                row.league = League.objects.get(league_name=match['League'])
                row.team_home = Team.objects.get(name=match['HomeTeam'])
                row.team_visitor = Team.objects.get(name=match['AwayTeam'])
                row.round = int(match['Round'])
                row.location = match['Location']
                row.xmlsoccer_matchid = match['Id']
                
                try:
                    row.score_home = match['HomeGoals']
                    row.score_visitor = match['AwayGoals']
                
                    if match['Time'] == 'Finished':
                        row.finished = True
                except KeyError:
                    pass
                
                row.save()
            except KeyError as e:
                print(str(e))
                        
    def clear(self):
        Match.objects.all().delete()
        League.objects.all().delete()
        Team.objects.all().delete()       
        
    def refreshAll(self):
        self.clear()
        self.LoadLeagues()
        self.LoadTeams()
        self.LoadMatches()
                
    def strToBool(self, str):
        return True if str.upper() == "TRUE" else False


def install():
    loader = Loader_Xmlsoccer('UQDWCTZTGRCJQQOSCXEESHVITEDGUYIVUVHYBFDBFOCLEGCATM')
    loader.refreshAll()

if __name__ == '__main__':
    print("This should only be run via django's ./manage.py shell.")

