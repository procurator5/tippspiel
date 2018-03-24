from django.core.management.base import BaseCommand
from tippspiel.install import Loader_Xmlsoccer


class Command(BaseCommand):
    help = """fix balances
"""

    def handle(self, **options):
        print("starting...")
        loader = Loader_Xmlsoccer('UQDWCTZTGRCJQQOSCXEESHVITEDGUYIVUVHYBFDBFOCLEGCATM')
        loader.loadActualInfo()



