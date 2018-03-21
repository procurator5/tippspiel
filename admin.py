from django.contrib import admin
from tippspiel.models import Team, Match, Tipp, MatchBet

class MatchBetInline(admin.TabularInline):
    model = MatchBet
    fk_name = 'match'
    extra=0
    readonly_fields=('bet', )
    fields = ('bet', 'score', 'min_value', 'max_value')

class MatchAdmin(admin.ModelAdmin):
    inlines = [MatchBetInline,]
    list_display = ('date', 'league', 'team_home', 'team_visitor', 'finished')

admin.site.register(Match, MatchAdmin)
admin.site.register(Team)
admin.site.register(Tipp)
