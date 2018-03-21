from django import template
from tippspiel.models import Tipp 

register = template.Library()

@register.inclusion_tag('tippspiel/modules/actual_bids.html', takes_context=True)
def actual_bids(context):
    request = context['request']
    tipps = []
    if request.user.is_authenticated:
        tipps = Tipp.objects.filter(player=request.user, state = 'In Game').all()
    return {'tipps': tipps}