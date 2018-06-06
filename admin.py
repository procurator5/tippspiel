from django.contrib import admin
from tippspiel.models import Match, Tipp, MatchBet, League

class MatchBetInline(admin.TabularInline):
    model = MatchBet
    fk_name = 'match'
    extra=0
    can_delete=False
    readonly_fields=('bet', 'amount', 'recomended_score')
    fields = ('bet', 'score', 'amount', 'recomended_score', 'min_value', 'max_value', 'is_enabled')

class MatchAdmin(admin.ModelAdmin):
    inlines = [MatchBetInline,]
    list_display = ('date', 'league', 'team_home', 'team_visitor', 'total_balance', 'finished')

admin.site.register(Match, MatchAdmin)
admin.site.register(Tipp)


class LeagueAdmin(admin.ModelAdmin):
    list_display =('league_name', 'country', 'is_enabled')
    list_editable = ('is_enabled',)

admin.site.register(League, LeagueAdmin)