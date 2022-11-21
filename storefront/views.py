from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from .forms import CustomizationForm

class HomePageView(TemplateView):
   template_name = "home.html"
    
class MenuPageView(ListView):
    model = Menu
    template_name = "menu.html"

def MenuHomePageView(request):
    return render(request, 'menu-home.html')

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

def ItemDetailView(request, pk):
    item = Menu.objects.get(pk = pk)
    
    # If it is a POST request we will process the form data
    if request.method == 'POST':
        # create a form and populate with data from the request
        form = CustomizationForm(request.POST)
 
        # check if the form is valid
        if form.is_valid():


            return render(request, 'menu-home.html')
    # If method is GET create a blank form
    else:
        form = CustomizationForm()
        
    return render(request, 'item-detail.html', {'item': item, 'form':form})

def LocationView(request):
    return render(request,'locations.html')

@staff_member_required
def AnalyticsPageView(request):
    return render(request, 'analytics.html')
