import os
from django.conf import settings
from django.core.management import BaseCommand

from xwing_data.tasks import FUNCTIONS, import_data


class Command(BaseCommand):
    help = "remove incompatible files after bower install"

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, username=None, *args, **options):
        os.remove(
            os.path.join(
                settings.BOWER_COMPONENTS_ROOT,
                'bower_components',
                'eonasdan-bootstrap-datetimepicker',
                'build',
                'css',
                'bootstrap-datetimepicker-standalone.css'
            )
        )
