from django.core.management.base import BaseCommand

from .scripts.delete_dublicates_modifications import delete_duplicates_modifications
from .scripts.import_brand import import_brands
from .scripts.import_categories import import_categories
from .scripts.import_generations import import_generations
from .scripts.import_models import import_models
from .scripts.import_modifications import import_modifications


class Command(BaseCommand):

    def handle(self, **options):    # noqa: WPS110
        import_categories()
        import_brands()
        import_models()
        import_generations()
        import_modifications()
        delete_duplicates_modifications()
