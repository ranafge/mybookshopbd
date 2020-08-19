from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator
from django.views.generic.list import MultipleObjectMixin
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.core.mail import send_mail
from django.views import generic
from . import models
from . import forms
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import string, random
import pdb
from django.db.models import Count
from django.db.models import Q


def market(request):
    return {
        "all_publication": models.Publication.objects.all(),
        "all_author": models.Author.objects.all(),
        "all_category": models.Category.objects.all(),
        "discount_books":models.Bookstore.objects.filter(discount_price__gt=1).all()
    }
