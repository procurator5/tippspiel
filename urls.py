from django.conf.urls import url
from django.contrib.auth import views as auth
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, TemplateView
from tippspiel.models import Team, Match, Tipp
from tippspiel.views import *

urlpatterns = [
    url(
        r'^$',
        matches,
        name='tippspiel_match_list'        
    ),
    url(
        r'^matches/$',
        overview,
        name="tippspiel_overview"
    ),
    url(
        r'^matches/data$',
        json_data,
        name="tippspiel_json"
    ),
    url(
        r'^match/(?P<match_id>\d+)/$',
        match_detail,
        name="tippspiel_match_detail"
    ),

    url(
        r'^search/$',
        search,
        name="search"
    ),

    url(
        r'^bet/(?P<bet_id>\d+)/$',
        bet_info,
        name="tippspiel_bet_info"
    ),

    url(
        r'^bid/(?P<bet_id>\d+)/$',
        bet_form,
        name="tippspiel_bet_form"
    ),

    url(
        r'^bet_res/$',
        bet_save,
        name="tippspiel_bet_result"
    ),

    url(
        r'^betSell/(?P<bet_id>\d+)/$',
        bet_sell,
        name="bet_sell"
    ),
]