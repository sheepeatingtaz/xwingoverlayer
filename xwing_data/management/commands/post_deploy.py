import os
from django.conf import settings
from django.core.management import BaseCommand, call_command

from xwing_data.tasks import FUNCTIONS, import_data


class Command(BaseCommand):
    help = "remove incompatible files after bower install"

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, username=None, *args, **options):
        call_command('migrate')
        call_command('bower', 'install')
        call_command('import_xwing_data')
        call_command('clean_bower')
        call_command('collectstatic', verbosity=0, interactive=False)

