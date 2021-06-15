from django import template

register = template.Library()

from ..models import *
from django.shortcuts import render


@register.simple_tag
def isFavourite(request, tutor):
    if tutor.favourite_set.filter(user=request.user):
        return 1
    else:
        return 0

