from django.test import TestCase

import os
import json
from matches.tasks import import_squad
from django.conf import settings


def test_import(list):
    file = os.path.join(settings.PROJECT_ROOT, "squads", list)
    with open(file, encoding="utf8") as raw_data:
        data = json.load(raw_data)
    import_squad(data, "Jim Loves U-wings")
