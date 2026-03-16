import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings
from services.models import Service


class Command(BaseCommand):
    help = "Load services from CSV file"

    def handle(self, *args, **kwargs):

        file_path = os.path.join(
            settings.BASE_DIR,
            "services",
            "data",
            "services.csv"
        )

        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                Service.objects.get_or_create(name=row["name"])

        self.stdout.write(self.style.SUCCESS("Services successfully loaded"))