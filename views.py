# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext
from django.utils import timezone

from tippspiel.models import Match, Tipp, League, MatchBet, BetGroup

from django import template


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
            'league_list': league_list
        },
    )


#@login_required
#@csrf_protect
def league_detail(request, league_id):
    matches = Match.objects.filter(league=League.objects.get(id = int(league_id)))
    tipps = Tipp.objects.filter(player__user=request.user)
    tipps_by_matches = {t.match.pk: t for t in tipps}

    return render(
        request,
        'tippspiel/matchday_detail.html',
        {
            'number': league_id,
            'matches': matches,
            'tipps': tipps_by_matches
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
            'groups': BetGroup.objects.all(),
            'tip': match_bet
        },
    )

#@login_required
def match_detail(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    tipps = MatchBet.objects.filter(match=match).order_by('bet__bet_group')
    return render(
        request,
        'tippspiel/match_detail.html',
        {
            'match': match,
            'tipps': tipps,
            'groups': BetGroup.objects.all()
        },
    )

@login_required
def settings(request):
    errors = []
    return render_to_response(
        'tippspiel/settings.html',
        {
            'errors': errors
        },
        RequestContext(request)
    )
