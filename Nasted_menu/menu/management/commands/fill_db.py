from django.core.management.base import BaseCommand

from menu.models import Category


def create_from_dict(v, parent=None):
    for k, value in v:
        new_category, check = Category.objects.get_or_create(name=k, parent=parent)
        if v:
            create_from_dict(value.items(), parent=new_category)


class Command(BaseCommand):
    help = 'Fill database with some test data'

    def handle(self, *args, **options):
        products = {
            "Products": {
                "vegetables": {
                    "tomatoes": {
                        "red": {},
                        "yellow": {},
                    },
                },
                "fruits": {
                    "pears": {},
                    "apples": {
                        "red": {},
                        "green": {},
                        "colored": {},
                    },
                    "bananas": {},
                },
                "meat": {
                    "beef": {
                        "fresh": {},
                        "ground meat": {},
                    },
                    "pork": {
                        "fresh": {},
                        "ground meat": {},
                    },
                },
            }
        }

        cars = {
            "Cars": {
                "Japanese": {
                    "Suzuki": {},
                    "Toyota": {},
                },
                "German": {
                    "BMW": {},
                    "Audi": {},
                    "Mercedes": {},
                },
                "Russian ": {
                    "Lada": {},
                    "Niva": {},
                },
            }
        }

        v = products.items()
        create_from_dict(v)
        v = cars.items()
        create_from_dict(v)

        return 'OK'
