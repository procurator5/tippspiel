from django.core.management.base import BaseCommand
from tippspiel.install import Loader_Xmlsoccer
from tippspiel.models import Match
from bet.settings import XMLSOCCER_DEMO


class Command(BaseCommand):
    help = """fix balances
"""

    def handle(self, **options):
        print("starting...")
        loader = Loader_Xmlsoccer('UQDWCTZTGRCJQQOSCXEESHVITEDGUYIVUVHYBFDBFOCLEGCATM', XMLSOCCER_DEMO)        
        loader.loadActualInfo()


