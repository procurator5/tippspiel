# coding=utf-8

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

from tippspiel.models import Player, Team, Match, Tipp, League

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

    return render_to_response(
        'tippspiel/overview.html',
        {
            'league_list': league_list
        },
        RequestContext(request)
    )


#@login_required
#@csrf_protect
def league_detail(request, league_id):


    matches = Match.objects.filter(league=League.objects.get(id = int(league_id)))
    tipps = Tipp.objects.filter(player__user=request.user)
    tipps_by_matches = {t.match.pk: t for t in tipps}

    return render_to_response(
        'tippspiel/matchday_detail.html',
        {
            'number': league_id,
            'matches': matches,
            'tipps': tipps_by_matches
        },
        RequestContext(request)
    )

#@login_required
#@csrf_protect
def matches(request):


    matches = Match.objects.all().order_by("date")

    return render_to_response(
        'tippspiel/matches_list.html',
        {
            'matches': matches,
        },
        RequestContext(request)
    )

@login_required
def match_detail(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    tipps = None
    if match.has_started():
        tipps = Tipp.objects.filter(match=match).order_by('player__rank')
    return render_to_response(
        'tippspiel/match_detail.html',
        {
            'match': match,
            'tipps': tipps
        },
        RequestContext(request)
    )


@login_required
def player_detail(request, player_name):
    p = get_object_or_404(Player, user__username=player_name)
    return render_to_response(
        'tippspiel/player_detail.html',
        {
            'player': p
        },
        context_instance=RequestContext(request)
    )

@login_required
def settings(request):
    errors = []
    if request.method == 'POST':
        npw = 1
        npw_c = 1
    return render_to_response(
        'tippspiel/settings.html',
        {
            'errors': errors
        },
        RequestContext(request)
    )


@staff_member_required
def update_scores_and_ranks(request):
    # update scores
    for player in Player.objects.all():
        player.update_score()
        player.save()

    # update ranks
    players = Player.objects.all().order_by('score').reverse()
    rank, tick, score = 1, 0, players[0].score
    for player in players:
        if player.score < score:
            rank += tick
            tick = 1
            score = player.score
        else:
            tick += 1
        if player.rank != rank:
            player.rank = rank
            player.save()

    return HttpResponseRedirect(reverse('tippspiel_settings'))
