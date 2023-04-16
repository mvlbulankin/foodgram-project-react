import csv

from django.core.management import BaseCommand

from ingredients.models import Ingredient
from tags.models import Tag


class Command(BaseCommand):
    help = "Добавление в БД дефолтного датасета с ингридиентами и тегами"

    def add_arguments(self, parser):
        parser.add_argument(
            "--use_default_dataset",
            action="store_true",
            help="use it to default dataset upload",
        )

    def handle(self, *args, **options):
        with open("static/data/ingredients.csv", "rt", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                Ingredient.objects.create(name=row[0], measurement_unit=row[1])
        with open("static/data/tags.csv", "rt", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                Tag.objects.create(name=row[0], color=row[1], slug=row[2])
