# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_protect

from tippspiel.models import Match, Tipp, League, MatchBet
from tippspiel.forms import SearchForm

from django import template
import decimal


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

def search(request):
    matches = None
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data['quote']
            matches = Match.objects.search(q)
    return render(
        request,
        'tippspiel/search.html',
        {
            'matches': matches,
        },
    )

@login_required
@csrf_protect
def bet_save(request):
    try:
        if request.method != 'POST':
            raise Exception("Error getting parameters. Go back to the options page and try again")
        
        betId = int(request.POST.get("betId"))
        betCount = decimal.Decimal(request.POST.get("betCount"))            
        bet = MatchBet.objects.get(pk=betId)  
        if bet.match.finished == True:
            raise Exception("Match has finished")     
        Tipp.create(request.user, bet, betCount)

        return render(
            request,
            'tippspiel/bet_save.html',
            {
                "is_error": False,
                'message': "Your bid has been successfully accepted.",
            },
        )
    
    except Exception as e:
        return render(
            request,
            'tippspiel/bet_save.html',
            {
                "is_error": True,
                'message': str(e),
            },
        )

@login_required
@csrf_protect
def bet_sell(request, bet_id):
    try:
        bet = Tipp.objects.get(pk=bet_id, player=request.user, state='In Game')
        bet.sell()
        
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
    matches = Match.objects.filter(league__is_enabled = True).filter(finished  = False).all().order_by("date")
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
    if match.finished==True:
        return redirect('account_activation_sent')

    tipps = MatchBet.objects.filter(match=match).order_by('bet__bet_group')
    
    return render(
        request,
        'tippspiel/bet_form.html',
        {
            'match': match,
            'tipps': tipps,
            'tip': match_bet,
            'matchbets': match.getAllBets(),
            'bets': Tipp.objects.filter(player=request.user, state = 'In Game').all(),
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
            'matchbets': match.getAllBets(),
        },
    )
