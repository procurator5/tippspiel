#!/usr/bin/env python
# coding=utf-8
from tippspiel.xmlsoccer import XmlSoccer

from tippspiel.models import League, Team, Match, MatchBet, MatchBetHelper
from django.utils import timezone
from datetime import timedelta
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
            
    def LoadMatches(self, startDateString, endDateString):
        # I define current date/time (startDateString) and current date +2 mouths (endDateString)
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
                    row.timeinfo = match['Time']
                
                    if match['Time'] == 'Finished':
                        if row.finished == False:
                            row.finished = True
                            closed = row.closeMatch()
                            if closed:
                                row.save()
                except KeyError:
                    pass
                
                row.save()
                
            except KeyError as e:
                print(str(e))
            
            print(row.id)
            if row.needUpdateOdds():
                self.loadOddsForMatch(row)
                
            row.updateOdds()                                    
                            
    def clear(self):
        Match.objects.all().delete()
        League.objects.all().delete()
        Team.objects.all().delete()       
        
    def refreshAll(self):
        self.clear()
        self.LoadLeagues()
        self.LoadTeams()

        startDateString = timezone.now().isoformat()
        endDateString = (timezone.now() + timedelta(days=58)).isoformat()   
        
        self.LoadMatches(startDateString, endDateString)
                
    def strToBool(self, str):
        return True if str.upper() == "TRUE" else False
    
    def loadOddsForMatch(self, match):
        saved = False
        odds = self.loader.GetAllOddsByFixtureMatchId(fixtureMatch_Id=match.xmlsoccer_matchid)
        for odd in odds:
            print(odd)
            for bet in MatchBet.objects.filter(match = match, bet__bet_group__bet_name = odd['Type']).all():
                try:
                    bethelper = MatchBetHelper()
                    bethelper.bookmaker = odd["Bookmaker"]
                    bethelper.updated=odd['UpdatedDate']
                    bethelper.score = float(odd[bet.bet.xmlsoccer_tagname])
                    bethelper.matchbet=bet
                    bethelper.save()
                    saved=True
                except KeyError:
                    pass
        if saved:
            MatchBet.objects.filter(match=match).update(update=timezone.now())

    def loadActualInfo(self):        
        #startDateString  = Match.objects.filter(finished = False).all().aggregate(Min('date'))['date__min']
        #endDateString = (timezone.now() + datetime.timedelta(days=1))
        startDateString = (timezone.now() - timedelta(days=2))
        endDateString = (timezone.now() + timedelta(days=50))   
        if endDateString > startDateString:
            self.LoadMatches(startDateString.isoformat(), endDateString.isoformat())

def install():
    loader = Loader_Xmlsoccer('UQDWCTZTGRCJQQOSCXEESHVITEDGUYIVUVHYBFDBFOCLEGCATM')
    loader.refreshAll()
    
def actual():
    loader = Loader_Xmlsoccer('UQDWCTZTGRCJQQOSCXEESHVITEDGUYIVUVHYBFDBFOCLEGCATM')
    loader.loadActualInfo()

def update():
    loader = Loader_Xmlsoccer('UQDWCTZTGRCJQQOSCXEESHVITEDGUYIVUVHYBFDBFOCLEGCATM')
    startDateString = timezone.now().isoformat()
    endDateString = (timezone.now() + timedelta(days=58)).isoformat()   
        
    loader.LoadMatches(startDateString, endDateString)

    loader.loadActualInfo()

if __name__ == '__main__':
    print("This should only be run via django's ./manage.py shell.")

