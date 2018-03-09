from django.conf.urls import url
from django.contrib.auth import views as auth
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, TemplateView
from tippspiel.models import Player, Team, Match, Tipp
from tippspiel.views import *


urlpatterns = [
    url(
        r'^login/$',
        auth.login,
        {
            'template_name': 'tippspiel/login.html'
        },
        name='login'
    ),
   
    url(
        r'^logout/$',
        auth.logout_then_login,
        name="logout"
    ),
    
    url(
        r'^changepw/$',
        auth.password_change,
        {
            'template_name': 'tippspiel/password_change.html',
            'post_change_redirect' : '/tippspiel/settings/'
        },
        name="password_change"
    ),
]

urlpatterns += [
    url(
        r'^$',
        overview,
        name="tippspiel_overview"
    ),

    url(
        r'^matchdays/$',
        login_required(ListView.as_view(
            queryset=range(1, 35),
            context_object_name='matchdays',
            template_name='tippspiel/matchday_list.html'
        )),
        name="tippspiel_matchday_list"
    ),

    url(
        r'^league/(?P<league_id>\d+)/$',
        league_detail,
        name="tippspiel_league_detail"
    ),

    url(
        r'^matches/$',
        login_required(ListView.as_view(
            queryset=Match.objects.order_by('date'),
            context_object_name='matches'
        )),
        name='tippspiel_match_list'
    ),

    url(
        r'^match/(?P<match_id>\d+)/$',
        match_detail,
        name="tippspiel_match_detail"
    ),

    url(
        r'^ranking/$',
        login_required(ListView.as_view(
            queryset=Player.objects.order_by('-score', 'user__username'),
            context_object_name='players',
            template_name='tippspiel/player_list.html'
        )),
        name="tippspiel_player_list"
    ),

    url(
        r'^player/(?P<player_name>\w+)/$',
        player_detail,
        name="tippspiel_player_detail"
    ),

    url(
        r'^settings/$',
        settings,
        name="tippspiel_settings"
    ),

    url(
        r'update_scores_and_ranks/$',
        update_scores_and_ranks,
        name="tippspiel_staff_update_scores_and_ranks"
    ),

]