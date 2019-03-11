from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

import datetime
class RaceView(View):

    def get(self, request, *args, **kwargs):
        name = kwargs['name']
        year = datetime.datetime.today().year

        return HttpResponse("Race View")
