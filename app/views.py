# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils import timezone
from django.views.generic import TemplateView


# Create your views here.
class HomePageView(TemplateView):

    def get(self, request, **kwargs):
        return render(request, 'index.html', context={'datetime': timezone.now()})


class AboutPageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'about.html', context=None)