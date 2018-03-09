from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.template.defaultfilters import default
from django.db.models.lookups import IsNull

class League(models.Model):
    league_name = models.CharField(max_length = 128)
    country = models.CharField(max_length = 128)
    is_cup = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=False)

class Player(models.Model):
    """A player is a user in the context of the tippspiel."""
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING,)
    score = models.IntegerField("The player's score.", default=0)
    rank = models.IntegerField("The player's rank", default=1)

    def gravatar_hash(self):
        from hashlib import md5
        try:
            return md5(self.user.email.lower()).hexdigest()
        except TypeError:
            return ""

    def update_score(self):
        tipps = Tipp.objects.filter(player=self)
        score = 0
        for tipp in tipps:
            score += tipp.points()
        self.score = score

    def __unicode__(self):
        return self.user.username


# connect signal
def create_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

post_save.connect(create_player, sender=User)



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
    score_home = models.IntegerField(default=-1)
    score_visitor = models.IntegerField(default=-1)

    def has_started(self):
        return self.date <= timezone.now()
        
    
    def __unicode__(self):
        return '%s %d:%d %s' % (self.team_home.handle, self.score_home, self.score_visitor, self.team_visitor.handle)



class Tipp(models.Model):
    """A bet by a player on a match."""
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    match = models.ForeignKey(Match, on_delete=models.DO_NOTHING)
    date = models.DateTimeField()
    score_home = models.IntegerField(default=0)
    score_visitor = models.IntegerField(default=0)

    def points(self):
        sh = self.match.score_home
        sv = self.match.score_visitor
        th = self.score_home
        tv = self.score_visitor
        if -1 in [sh, sv, th, tv]:
            return 0
        sgn = lambda x: 0 if x==0 else x/abs(x)
        points = 0
        ds = sh-sv
        dt = th-tv
        if sgn(ds)==sgn(dt):
            # correct tendency
            points += 1
            if ds==dt:
                # correct difference
                points += 1
                if sh==th:
                    # correct result
                    points += 1
        return points


    def __unicode__(self):
        return 'Tipp by %s on %s (%d:%d) (%d)' % (self.player, self.match, self.score_home, self.score_visitor, self.points())
