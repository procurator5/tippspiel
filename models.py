from django.contrib.auth.models import User
from django_bitcoin.models import Wallet, WalletTransaction
from django.db import models, connection
from django.utils import timezone
from bbil.models import Profile
import decimal

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

class League(models.Model):
    league_name = models.CharField(max_length = 128)
    country = models.CharField(max_length = 128)
    is_cup = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=False)
    
    def getActualMatches(self):
        return Match.objects.filter(league = self).filter(date__gte  = timezone.now()).order_by('date').all()

    def __str__(self):
        return self.league_name

    
class BetGroup(models.Model):
    bet_name = models.TextField()
    bet_short_name = models.CharField(max_length = 128)
    is_main = models.BooleanField(default=False)

class BetType(models.Model):
    bet_group = models.ForeignKey(BetGroup, on_delete=models.CASCADE)
    bet_choice = models.CharField(max_length = 128)
    order = models.IntegerField(default=1)
    min_value = models.DecimalField(
        max_digits=16,
        decimal_places=8,
        default=0.00001)
       
    max_value = models.DecimalField(
        max_digits=16,
        decimal_places=8,
        default=1.0)
    
    handler=models.CharField(max_length = 64, null=True)
    
    def __str__(self):
        return self.bet_group.bet_name + "- " + self.bet_choice

class Team(models.Model):
    """A team in the Bundesliga"""
    handle = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=128, default=None)
    stadium = models.CharField(max_length=128, null=True, default=None)

    def __str__(self):
        return self.name

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
    wallet = models.ForeignKey("django_bitcoin.Wallet", on_delete=models.DO_NOTHING)
    xmlsoccer_matchid = models.IntegerField()
    finished = models.BooleanField(default=False)
    started = models.BooleanField(default=True)

    def has_started(self):
        return self.date <= timezone.now()
        
    
    def __unicode__(self):
        return '%s %d:%d %s' % (self.team_home.handle, self.score_home, self.score_visitor, self.team_visitor.handle)
    
    # this is not needed if small_image is created at set_image
    def save(self, *args, **kwargs):
        self.wallet, created = Wallet.objects.get_or_create(label=self.team_home.name+"-"+self.team_visitor.name)
        recv_address = self.wallet.receiving_address(fresh_addr=False)
        super(Match, self).save(*args, **kwargs)
        # I write bets coefficients in table 
        if MatchBet.objects.filter(match=self).count()== 0:
            for bet in BetType.objects.all():
                row = MatchBet(match=self, bet=bet, max_value= bet.max_value, min_value=bet.min_value)
                row.save()

    def closeMatch(self):
        if self.finished ==True:
            result = True
            bank_profile = Profile.objects.filter(user__is_superuser=True).first()
            for tip in Tipp.objects.filter(match=self, status="In Game"):
                closed = tip.close(bank_profile.wallet)
                result &= closed
            if self.wallet.total_balance()>0:
                self.wallet.send_to_wallet(bank_profile.wallet, self.wallet.total_balance())
            return result
        return False 
    
    #Coefficient bid for             
    def getMainBets(self):
        bets = BetType.objects.filter(bet_group__is_main = True).all()
        return MatchBet.objects.filter(match = self).filter(bet__in = bets).order_by('bet__order').all()
    
    
class MatchBet(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    bet = models.ForeignKey(BetType, on_delete=models.CASCADE)
    score = models.FloatField(default = 1.0)
    min_value = models.DecimalField(
        max_digits=16,
        decimal_places=8,
        default=0.00001)
       
    max_value = models.DecimalField(
        max_digits=16,
        decimal_places=8,
        default=1.0)
    
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
    transaction = models.ForeignKey("django_bitcoin.WalletTransaction", on_delete=models.DO_NOTHING, null=True)

    def isWin(self):
        return False
    
    def close(self, bank_wallet):
        if self.isWin():
            bitcoin_amount = self.amount * decimal.Decimal(self.score)
            if bitcoin_amount > self.match.wallet.total_balance():
                bank_wallet.send_to_wallet(self.match.wallet, bitcoin_amount - self.wallet.total_balance())
                
            player = Profile.objects.get(user = self.player)    
            self.match.wallet.send_to_wallet(player.wallet, bitcoin_amount)
            self.status="Win"
        else:
            bitcoin_amount = self.match.wallet.total_balance() if self.amount > self.match.wallet.total_balance() else self.amount
            self.match.wallet.send_to_wallet(bank_wallet, bitcoin_amount)
                    
            self.status="Lose"

            
        self.save()    
    
    def sell(self):
        try:
            self.match.wallet.send_to_wallet(self.player.wallet, self.amount * decimal.Decimal(0.9))
            self.state = "Sold"
            self.save()
            return True
        except Exception:
            return False
