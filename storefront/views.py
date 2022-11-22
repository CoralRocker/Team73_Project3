from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.admin.views.decorators import staff_member_required

from .models import *
from .forms import CustomizationForm
    
class MenuPageView(ListView):
    model = Menu
    template_name = "menu.html"

def HomePageView(request):
    hasCart = False
    try:
        if 'cart' in request.session:
            Order.objects.get(pk=request.session['cart'])
            hasCart = True
    except:
        print("Either no cart exists or it is invalid")
    return render(request, 'home.html', {'hasCart': hasCart})

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
            amount = 1
            size = 'grande'
            for key, value in form.cleaned_data.items():
                if key == 'size':
                    if value and value != '':
                        size
                elif key[0:3] != 'amt':
                    if value and value != '':
                        if value != 'milk':
                            amount_string = 'amt_' + value
                            amount = form.cleaned_data[amount_string]
                        OrderItem.objects.get(pk=request.session['item-in-view']).addCustomization(Customization.objects.get(id=value),amount)
            del request.session['item-in-view']

            return render(request, 'menu-home.html', {'hasCart':hasCart})
    # If method is GET create a blank form
    else:
        form = CustomizationForm()
        
    return render(request, 'item-detail.html', {'item': item, 'form':form, 'hasCart':hasCart})

def LocationView(request):
    hasCart = False
    try:
        if 'cart' in request.session:
            Order.objects.get(pk=request.session['cart'])
            hasCart = True
    except:
        print("Either no cart exists or it is invalid")
    return render(request,'locations.html', {'hasCart': hasCart})

@staff_member_required
def AnalyticsPageView(request):
    return render(request, 'analytics.html', {'hasCart':False})

def CheckoutPageView(request):
    order = Order.objects.get(pk=request.session['cart'])
    # Remove unadded items from cart
    if request.method == 'POST':
        data = request.POST
        if "remove-id" in data:
            item = data.get("remove-id")
            OrderItem.objects.get(id=int(item)).delete()
        elif "checkingout" in data:
            del request.session['cart']
            return redirect('home')
      
    return render(request, 'checkout.html', {'order': order, 'hasCart':False})
