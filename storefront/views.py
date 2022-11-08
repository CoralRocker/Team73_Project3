from django.shortcuts import render
from django.views.generic import TemplateView, ListView
# from .models import MenuItem

class HomePageView(TemplateView):
   template_name = "home.html"
    
# class MenuPageView(ListView):
#     model = MenuItem
#     template_name = "menu.html"

