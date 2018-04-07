from django.shortcuts import render
from django.views import generic
from games.models import GameData

# class TeachView(generic.TemplateView):
#     template_name = 'project/teach.html'
class TeachView(generic.ListView):
    template_name = 'project/teach.html'
    def get_queryset(self):
        return GameData.objects.all()
