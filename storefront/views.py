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
    if 'item-in-view' in request.session:
        try:
            OrderItem.objects.get(pk=request.session['item-in-view']).delete()
        except:
            print("It looks like the orderitem is already deleted...")
            del request.session['item-in-view']

    hasCart = False
    try:
        if 'cart' in request.session:
            Order.objects.get(pk=request.session['cart'])
            hasCart = True
    except:
        print("Either no cart exists or it is invalid")

    return render(request, 'menu-home.html', {'hasCart': hasCart})

def EspressoPageView(request):
    if 'item-in-view' in request.session:
        try:
            OrderItem.objects.get(pk=request.session['item-in-view']).delete()
        except:
            print("It looks like the orderitem is already deleted...")
            del request.session['item-in-view']

    hasCart = False
    try:
        if 'cart' in request.session:
            Order.objects.get(pk=request.session['cart'])
            hasCart = True
    except:
        print("Either no cart exists or it is invalid")

    products = Menu.objects.filter(type__iexact="espresso", size__iexact="grande") | Menu.objects.filter(type__iexact="espresso", size__iexact="doppio")
    return render(request, 'espresso.html', {'products':products, 'hasCart':hasCart})

def BrewedPageView(request):
    if 'item-in-view' in request.session:
        try:
            OrderItem.objects.get(pk=request.session['item-in-view']).delete()
        except:
            print("It looks like the orderitem is already deleted...")
            del request.session['item-in-view']

    hasCart = False
    try:
        if 'cart' in request.session:
            Order.objects.get(pk=request.session['cart'])
            hasCart = True
    except:
        print("Either no cart exists or it is invalid")

    products = Menu.objects.filter(type__iexact="brewed", size__iexact="grande")
    return render(request, 'brewed.html', {'products':products, 'hasCart':hasCart})

def BlendedPageView(request):
    if 'item-in-view' in request.session:
        try:
            OrderItem.objects.get(pk=request.session['item-in-view']).delete()
        except:
            print("It looks like the orderitem is already deleted...")
            del request.session['item-in-view']

    hasCart = False
    try:
        if 'cart' in request.session:
            Order.objects.get(pk=request.session['cart'])
            hasCart = True
    except:
        print("Either no cart exists or it is invalid")

    products = Menu.objects.filter(type__iexact="blended", size__iexact="grande")
    return render(request, 'blended.html', {'products':products, 'hasCart':hasCart})

def TeaPageView(request):
    if 'item-in-view' in request.session:
        try:
            OrderItem.objects.get(pk=request.session['item-in-view']).delete()
        except:
            print("It looks like the orderitem is already deleted...")
            del request.session['item-in-view']
    
    hasCart = False
    try:
        if 'cart' in request.session:
            Order.objects.get(pk=request.session['cart'])
            hasCart = True
    except:
        print("Either no cart exists or it is invalid")
    
    products = Menu.objects.filter(type__iexact="tea", size__iexact="grande")
    return render(request, 'tea.html', {'products':products, 'hasCart':hasCart})

def OtherPageView(request):
    if 'item-in-view' in request.session:
        try:
            OrderItem.objects.get(pk=request.session['item-in-view']).delete()
        except:
            print("It looks like the orderitem is already deleted...")
            del request.session['item-in-view']
    
    hasCart = False
    try:
        if 'cart' in request.session:
            Order.objects.get(pk=request.session['cart'])
            hasCart = True
    except:
        print("Either no cart exists or it is invalid")

    products = Menu.objects.filter(type__iexact="other", size__iexact="grande")
    return render(request, 'other.html', {'products':products, 'hasCart':hasCart})

def ItemDetailView(request, pk):
    item = Menu.objects.get(pk = pk)
    
    hasCart = False
    try:
        if 'cart' in request.session:
            Order.objects.get(pk=request.session['cart'])
            hasCart = True
    except:
        print("Either no cart exists or it is invalid")

    # Create Cart if it doesn't exist
    if 'cart' not in request.session:
        request.session['cart'] = Order.create('user-created').pk

    # Create Temporary Item Session
    # Create if item is different than previous, or if doesn't exist
    if 'item-in-view' not in request.session or OrderItem.objects.get(pk=request.session['item-in-view']).menu_item.name != item.name:

        # Delete Previous Items
        if 'item-in-view' in request.session:
            OrderItem.objects.get(pk=request.session['item-in-view']).delete()

        order = int(request.session['cart'])
        request.session['item-in-view'] = OrderItem.create(
                Order.objects.get(pk=order), # Create orderItem belonging to cart
                item).pk # Create with menu item selected

    
    # If it is a POST request we will process the form data
    if request.method == 'POST':
        # create a form and populate with data from the request
        form = CustomizationForm(request.POST)
        # check if the form is valid
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                if value and value != '':
                    OrderItem.objects.get(pk=request.session['item-in-view']).addCustomization(Customization.objects.get(id=value),1)
            del request.session['item-in-view']

            return render(request, 'menu-home.html', {'hasCart':hasCart})
    # If method is GET create a blank form
    else:
        form = CustomizationForm()
        
    return render(request, 'item-detail.html', {'item': item, 'form':form, 'hasCart':hasCart})

def LocationView(request):
    return render(request,'locations.html')

@staff_member_required
def AnalyticsPageView(request):
    return render(request, 'analytics.html', {'hasCart':False})

def CheckoutPageView(request):
    order = Order.objects.get(pk=request.session['cart'])
    # Remove unadded items from cart
    if request.method == 'POST':
        data = request.POST
        item = data.get("remove-id")
        OrderItem.objects.get(id=int(item)).delete()
    
    
    return render(request, 'checkout.html', {'order': order, 'hasCart':False})
