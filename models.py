from django.contrib.auth.models import User
from django_bitcoin.models import Wallet, WalletTransaction
from django.db import models, connection
from django.db.models import Q, Min
from django.utils import timezone
from bbil.models import Profile
import decimal

from datetime import timedelta


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
    xmlsoccer_tagname = models.CharField(max_length=64, null=True)
    
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
    
    def minutes(self):
        if self.has_started():
            return (timezone.now() - self.date).seconds//60
        return 0
        
    def times(self):
        if self.has_started():
            return self.minutes()//45 +1
        return "NoN"
    
    def __str__(self):
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
            for tip in Tipp.objects.filter(match=self, state="In Game"):
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
    
    def getAllBets(self):
        return MatchBet.objects.filter(match=self).filter(models.Q(bet__bet_group__is_main = True) | models.Q(is_enabled=True)).order_by("id").all()
    
    def total_balance(self):
        return self.wallet.total_balance()
    
    def needUpdateOdds(self):
        if MatchBet.objects.filter(match = self).filter( Q( update__isnull = True) | Q(update__lte = timezone.now() - timedelta(days=1))).count() == 0:
            return False
        return True
    
    def updateOdds(self):
        for bet in MatchBet.objects.filter(match = self).all():
            bet.calculate()
    
    
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
    
    is_enabled=models.BooleanField(default=True)
    update = models.DateTimeField(null=True)
    is_manual = models.BooleanField(default = False)
    
    def amount(self):
        this_amount = Tipp.objects.filter(bet = self.bet, match=self.match, state="In Game").all().aggregate(models.Sum('amount'))['amount__sum']
        return 0 if this_amount == None else this_amount
    
    def recomended_score(self):
        this_amount = self.amount()
        if this_amount <= 0:
            return "0/x"
        that_amount = self.match.total_balance() - this_amount
        if that_amount <= 0:
            return "x/0"
        return float((self.match.total_balance() * decimal.Decimal(0.9))/this_amount)
    
    def calculate(self):
        if self.is_manual ==False:
            score = MatchBetHelper.objects.filter(matchbet=self).all().aggregate(Min('score'))['score__min']
            score = round(0 if score ==None else score, 2)
            if score > 1:
                self.score=score
                self.save()
    
class MatchBetHelper(models.Model):
    matchbet = models.ForeignKey(MatchBet, on_delete=models.CASCADE)
    bookmaker = models.CharField(max_length=64)    
    updated = models.DateTimeField(null=True)
    score = models.FloatField(default=0)
    
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

    def isWin(self):
        c = connection.cursor()
        try:
            c.callproc("iswin", (self.id, ))
            results = c.fetchall()
            c.close()
            return results[0][0]
        except Exception:
            c.close()
            return False
    
    def close(self, bank_wallet):
        transaction = None
        if self.isWin():
            bitcoin_amount = round(self.amount * decimal.Decimal(self.bet_score), 8)
            if bitcoin_amount > self.match.wallet.total_balance():
                bank_wallet.send_to_wallet(self.match.wallet, bitcoin_amount - self.match.wallet.total_balance())
                
            player = Profile.objects.get(user = self.player)    
            self.match.wallet.send_to_wallet(player.wallet, bitcoin_amount)
            self.state="Win"
        else:
            bitcoin_amount = round(self.match.wallet.total_balance() if self.amount > self.match.wallet.total_balance() else self.amount, 8)
            if bitcoin_amount > 0: 
                self.match.wallet.send_to_wallet(bank_wallet, bitcoin_amount)
                    
            self.state="Lose"

            
        self.save()

        state = TippState()
        state.tipp = self
        state.state = self.state
        state.transaction = transaction
        state.save()
        
        return True    
    
    def sell(self):
        
        player = Profile.objects.get(user = self.player)    
        transaction = self.match.wallet.send_to_wallet(player.wallet, self.amount * decimal.Decimal(0.9))
        self.state = "Sold"
        self.save()
            
        #add new TippState
        state = TippState()
        state.tipp = self
        state.state = self.state
        state.transaction = transaction
        state.save()
    
    def toAccount(self):
        if self.state == "Sold":
            return round(self.amount *  decimal.Decimal(0.9), 8)
        if self.state == "Win": 
            return round(self.amount * decimal.Decimal(self.bet_score), 8)
        if self.state == "In Game":
            return "In Game"
        return 0 
        
    @staticmethod
    def create(user, bet, amount):
        if amount > bet.min_value and amount<bet.max_value:
            # Make transaction
            profile = Profile.objects.get(user=user)
            if profile.wallet.total_balance()>=amount:
                row =Tipp()
                transaction = profile.wallet.send_to_wallet(bet.match.wallet, amount)
                
                row.player = user
                row.bet_score = bet.score
                row.match = bet.match
                row.amount = amount
                row.bet = bet.bet
                row.save()
                
                #add new TippState
                state = TippState()
                state.tipp = row
                state.transaction = transaction
                state.save()                
            else:
                raise Exception("Your balance does not have enough funds to bid")
        else:
            raise Exception("Your bet is too small or too high. Change the amount and try again")        
        
class TippState(models.Model):
    tipp = models.ForeignKey(Tipp, on_delete=models.DO_NOTHING)
    state = models.CharField(max_length=128, default='InGame')
    date = models.DateTimeField(default = timezone.now)
    transaction = models.ForeignKey("django_bitcoin.WalletTransaction", on_delete=models.DO_NOTHING, null=True)
    

