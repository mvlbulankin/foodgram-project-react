import csv
from collections import OrderedDict

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from ingredients.models import Ingredient
from tags.models import Tag


MODELS_FIELDS = {
    'ingredient': Ingredient,
    'tag': Tag,
}

DEFAULT_DATASET = OrderedDict({
    'ingredients.csv': Ingredient,
    'tags.csv': Tag,
})

DEFAULT_DATASET_PATH = 'static/data/'


class Command(BaseCommand):
    help = "Добавление в БД дефолтного датасета с ингридиентами и тегами"

    @staticmethod
    def dict_reader_csv(csv_file, model):
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            for field, value in row.items():
                if field in MODELS_FIELDS.keys():
                    row[field] = get_object_or_404(
                        MODELS_FIELDS[field], pk=value
                    )
            model.objects.create(**row)

    def add_arguments(self, parser):
        parser.add_argument(
            "--use_default_dataset",
            action="store_true",
            help="use it to default dataset upload",
        )

    def handle(self, *args, **options):
        for filename, model in DEFAULT_DATASET.items():
            with open(
                    DEFAULT_DATASET_PATH + filename, 'rt', encoding='utf-8'
            ) as csv_file:
                self.dict_reader_csv(csv_file, model)
