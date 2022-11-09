from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.admin.views.decorators import staff_member_required
from .models import *


class HomePageView(TemplateView):
   template_name = "home.html"
    
class MenuPageView(ListView):
    model = Menu
    template_name = "menu.html"

def EspressoPageView(request):
    products = Menu.objects.filter(type__iexact="espresso", size__iexact="grande") | Menu.objects.filter(type__iexact="espresso", size__iexact="doppio")
    return render(request, 'espresso.html', {'products':products})

def BrewedPageView(request):
    products = Menu.objects.filter(type__iexact="brewed", size__iexact="grande")
    return render(request, 'brewed.html', {'products':products})

def BlendedPageView(request):
    products = Menu.objects.filter(type__iexact="blended", size__iexact="grande")
    return render(request, 'blended.html', {'products':products})

def TeaPageView(request):
    products = Menu.objects.filter(type__iexact="tea", size__iexact="grande")
    return render(request, 'tea.html', {'products':products})

def OtherPageView(request):
    products = Menu.objects.filter(type__iexact="other", size__iexact="grande")
    return render(request, 'other.html', {'products':products})

@staff_member_required
def AnalyticsPageView(request):
    return render(request, 'analytics.html')