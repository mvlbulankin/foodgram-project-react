import csv

from django.core.management import BaseCommand
from ingredients.models import Ingredient


class Command(BaseCommand):
    help = 'Добавление в БД дефолтного датасета с ингридиентами'

    def add_arguments(self, parser):
        parser.add_argument(
            '--use_default_dataset',
            action='store_true',
            help="use it to default dataset upload"
        )

    def handle(self, *args, **options):
        with open('../data/ingredients.csv', 'rt', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                Ingredient.objects.create(name=row[0], measurement_unit=row[1])
