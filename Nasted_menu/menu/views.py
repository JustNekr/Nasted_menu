from pprint import pprint

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Category


def create_from_dict(v, parent=None):
    for k, value in v:
        new_category, check = Category.objects.get_or_create(name=k, parent=parent)
        if v:
            create_from_dict(value.items(), parent=new_category)


def create_tree(request):
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

    return render(request, template_name="index.html")


def show_category(request, pk=None):
    menu = None
    if pk:
        menu = Category.get_menu(pk)
    return render(request, template_name="index.html", context={'menu': menu})
