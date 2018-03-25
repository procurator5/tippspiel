from django.contrib import admin
from tippspiel.models import Team, Match, Tipp, MatchBet

class MatchBetInline(admin.TabularInline):
    model = MatchBet
    fk_name = 'match'
    extra=0
    readonly_fields=('bet', 'amount', 'recomended_score')
    fields = ('bet', 'score', 'amount', 'recomended_score', 'min_value', 'max_value')

class MatchAdmin(admin.ModelAdmin):
    inlines = [MatchBetInline,]
    list_display = ('date', 'league', 'team_home', 'team_visitor', 'total_balance', 'finished')

admin.site.register(Match, MatchAdmin)
admin.site.register(Team)
admin.site.register(Tipp)
