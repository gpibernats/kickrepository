from django.conf.urls import url
from django.urls import include, path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="project/homepage.html"), name="home"),
    path("teach", views.TeachView.as_view(), name="teach"),
]
