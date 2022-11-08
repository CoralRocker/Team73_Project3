from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Menu

class HomePageView(TemplateView):
   template_name = "home.html"
    
class MenuPageView(ListView):
    model = Menu
    template_name = "menu.html"

