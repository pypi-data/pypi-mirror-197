import json
import os

from django.conf import settings
from unittest import TestCase

from easys_ordermanager.v3.serializer import Serializer


class SerializerV3TestCase(TestCase):
    def setUp(self):
        with open(os.path.join(settings.BASE_DIR, 'dev', 'tests', 'v3', 'example.json'), 'r') as f:
            self.fixture = json.load(f)

    def test_validate_data(self):
        s = Serializer(data=self.fixture)
        self.assertTrue(s.is_valid(raise_exception=True))
