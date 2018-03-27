# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone

from tippspiel.models import Match, Tipp, League, MatchBet, BetGroup
from bbil.models import Profile

from django import template
import decimal
from bbil.views import profile
from django.template.context_processors import request


register = template.Library()


def active(url, request):
    if url == request.get_full_path():
        return True
    else:
        return False


register.filter('active', active)

#@login_required
def overview(request):
    league_list = League.objects.filter(is_enabled=True).all()

    return render(
        request,
        'tippspiel/overview.html',
        {
            'league_list': league_list,
        },
    )


@login_required
@csrf_protect
def bet_save(request):
    
    message = "Ваша ставка успешно принята."
    is_error = False

    if request.method == 'POST':
        betId = int(request.POST.get("betId"))
        betCount = float(request.POST.get("betCount"))
        
        bet = MatchBet.objects.get(pk=betId)
        if betCount > bet.min_value and betCount<bet.max_value:
            # Make transaction
            profile = Profile.objects.get(user=request.user)
            if profile.wallet.total_balance()>=betCount:
                row =Tipp()
                row.transaction = profile.wallet.send_to_wallet(bet.match.wallet, betCount)
                
                row.player = request.user
                row.bet_score = bet.score
                row.match = bet.match
                row.amount = betCount
                row.bet = bet.bet
                row.save()
            else:
                is_error = True
                message = "На вашем балансе не хватает средств для ставок"
        else:
            is_error = True
            message = "Ваша ставка слишком мала или слишком высока. Измените сумму и попробуйте снова"
                     
    else:
        is_error = True
        message = "Ошибка получения параметров. Вернитесь на страницу параметров и попробуйте снова"
        
    
    return render(
        request,
        'tippspiel/bet_save.html',
        {
            "is_error": is_error,
            'message': message,
        },
    )
@login_required
@csrf_protect
def bet_sell(request, bet_id):
    try:
        bet = Tipp.objects.get(pk=bet_id, player=request.user, state='In Game')
        profile = Profile.objects.get(user=request.user)
        bank_profile = Profile.objects.filter(user__is_superuser=True).first()
        bet.match.wallet.send_to_wallet(profile.wallet, bet.amount * decimal.Decimal(0.9))
        bet.state = "Sold"
        bet.save()
        bet.match.wallet.send_to_wallet(bank_profile.wallet, bet.amount * decimal.Decimal(0.1))
        
        return render(
            request,
            'tippspiel/bet_save.html',
            {
                "is_error": False,
                'message': "Ставка продана за "+ str(bet.amount * decimal.Decimal(0.9) )+" BTC",
            },
        )
    except Exception as e:
        return render(
            request,
            'tippspiel/bet_save.html',
             {
                "is_error": True,
                'message': "Ошибка при продаже ставки: "+ str(e),
            },
        )

#@login_required
#@csrf_protect
def matches(request):
    matches = Match.objects.filter(league__is_enabled = True).filter(date__gte  = timezone.now()).all().order_by("date")
    return render(
        request,
        'tippspiel/matches_list.html',
        {
            'matches': matches,
        },
    )

@login_required
def bet_info(request, bet_id):
    tip = get_object_or_404(Tipp, pk=bet_id)
    
    return render(
        request,
        'tippspiel/bet_info.html',
        {
            'tip': tip,
            'prize': decimal.Decimal(tip.bet_score) * tip.amount,
            'cancel':tip.amount * decimal.Decimal(0.9),
            
        },
    )


@login_required
def bet_form(request, bet_id):
    match_bet = get_object_or_404(MatchBet, pk=bet_id)
    match = match_bet.match
    tipps = MatchBet.objects.filter(match=match).order_by('bet__bet_group')
    
    return render(
        request,
        'tippspiel/bet_form.html',
        {
            'match': match,
            'tipps': tipps,
            'tip': match_bet,
            'matchbets': MatchBet.objects.filter(match=match).all()
        },
    )

#@login_required
def match_detail(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    return render(
        request,
        'tippspiel/match_detail.html',
        {
            'match': match,
            'matchbets': MatchBet.objects.filter(match=match).all()
        },
    )

@login_required
def bets_history(request):
    return render(
        request,
        'tippspiel/bets_history.html',
        {
            'tipps': Tipp.objects.filter(player=request.user).all()
        },
    )
    
