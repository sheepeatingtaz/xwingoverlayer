from django.core.management import BaseCommand

from xwing_data.models import Faction
from xwing_data.tasks import FUNCTIONS, import_data


class Command(BaseCommand):
    help = "Updates X-wing Data sources"

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, username=None, *args, **options):
        end_message = []
        
        # Extra step, just to make sure Faction names are stored for old versions
        for f in Faction.objects.all():
            f.save()

        for function_name, function in FUNCTIONS.items():
            print("Loading {}...".format(function_name))
            count = import_data(function_name, False)
            completed = "{} {} loaded".format(count, function_name)
            print(completed)
            end_message.append(completed)
        print("All Data Loaded: ")
        for msg in end_message:
            print(msg)
