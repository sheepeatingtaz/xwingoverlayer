from django.core.management import BaseCommand

from xwing_data.tasks import FUNCTIONS, import_data


class Command(BaseCommand):
    help = "Update users password"

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, username=None, *args, **options):
        for function_name, function in FUNCTIONS.items():
            print("Loading {}...".format(function_name))
            count = import_data(function_name, False)
            print("{} {} loaded".format(count, function_name))
        print("All Data Loaded.")
