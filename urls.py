from django.conf.urls import url
from django.contrib.auth import views as auth
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, TemplateView
from tippspiel.models import Team, Match, Tipp
from tippspiel.views import *


urlpatterns = [
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
        matches,
        name='tippspiel_match_list'        
    ),
    url(
        r'^matches/$',
        overview,
        name="tippspiel_overview"
    ),

    url(
        r'^match/(?P<match_id>\d+)/$',
        match_detail,
        name="tippspiel_match_detail"
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

]