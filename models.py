from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class League(models.Model):
    league_name = models.CharField(max_length = 128)
    country = models.CharField(max_length = 128)
    is_cup = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=False)
    
    def getActualMatches(self):
        return Match.objects.filter(league = self).filter(date__gte  = timezone.now()).order_by('date').all()
    
class BetGroup(models.Model):
    bet_name = models.TextField()
    bet_short_name = models.CharField(max_length = 128)
    is_main = models.BooleanField(default=False)

class BetType(models.Model):
    bet_group = models.ForeignKey(BetGroup, on_delete=models.CASCADE)
    bet_choice = models.CharField(max_length = 128)
    order = models.IntegerField(default=1)   

class Team(models.Model):
    """A team in the Bundesliga"""
    handle = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=128, default=None)
    stadium = models.CharField(max_length=128, null=True, default=None)

    def __unicode__(self):
        return self.handle

class Match(models.Model):
    """A match between two teams."""
    date = models.DateTimeField()
    league = models.ForeignKey(League, on_delete=models.CASCADE, null=True)
    matchday = models.IntegerField(default=0)
    team_home = models.ForeignKey(Team, related_name='+', on_delete=models.DO_NOTHING)
    team_visitor = models.ForeignKey(Team, related_name='+', on_delete=models.DO_NOTHING)
    round = models.IntegerField(default=1)
    location = models.CharField(max_length=128, null=True)
    score_home = models.IntegerField(default=0)
    score_visitor = models.IntegerField(default=0)

    def has_started(self):
        return self.date <= timezone.now()
        
    
    def __unicode__(self):
        return '%s %d:%d %s' % (self.team_home.handle, self.score_home, self.score_visitor, self.team_visitor.handle)
    
    # this is not needed if small_image is created at set_image
    def save(self, *args, **kwargs):
        super(Match, self).save(*args, **kwargs)
        # I write bets coefficients in table 
        for bet in BetType.objects.all():
            row = MatchBet(match=self, bet=bet)
            row.save()
    
    #Coefficient bid for             
    def getMainBets(self):
        bets = BetType.objects.filter(bet_group__is_main = True).all()
        return MatchBet.objects.filter(match = self).filter(bet__in = bets).order_by('bet__order').all()

class MatchBet(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    bet = models.ForeignKey(BetType, on_delete=models.CASCADE)
    score = models.FloatField(default = 1.0)
    


class Tipp(models.Model):
    """A bet by a player on a match."""
    
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default = timezone.now)
    state = models.CharField(max_length=128, default='In Game')
    bet = models.ForeignKey(BetType, on_delete=models.DO_NOTHING)
    bet_score = models.FloatField(default=1)
    amount = models.DecimalField(
        max_digits=16,
        decimal_places=8,
        default=0.0)


