import re

from django import template
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse, NoReverseMatch

from ..models import Category

register = template.Library()


@register.inclusion_tag('menu.html', takes_context=True)
def draw_menu(context: RequestContext, menu_name: str):
    """
    Draw tree menu
    :param menu_name:
    :param context:
    :type context: RequestContext
    :param name:
    :type name: str
    :param parent:
    :type parent: int
    :return:
    """

    menu = context.get('menu')
    if not menu or menu[0].menu_name != menu_name:
        menu = Category.objects.filter(menu_name=menu_name, parent=None)
    return {'menu': menu}
