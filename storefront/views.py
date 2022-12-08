""" this is the page that generates what is seen"""

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q

from .models import *
from .forms import CustomizationForm
    
class MenuPageView(ListView):
    model = Menu
    template_name = "menu.html"

# @brief generates the home page
#
# @param request The HTTP Request object from the website
# @return a render based on the reqeust, home.html, and a hash which is passed into the html
def HomePageView(request):
    hasCart = False
    try:
        if 'cart' in request.session:
            order = Order.objects.get(pk=request.session['cart'])
            hasCart = True
    except:
        print("Either no cart exists or it is invalid")
    return render(request, 'home.html', {'hasCart': hasCart, 'order':order})

# @brief generates the base page for menu
#
# @param request The HTTP Request object from the website
# @return a render based on the reqeust, home.html, and a hash which is passed into the html
def MenuHomePageView(request):
    if 'item-in-view' in request.session:
        try:
            OrderItem.objects.get(pk=request.session['item-in-view']).delete()
            del request.session['item-in-view']
        except:
            print("It looks like the orderitem is already deleted...")
            del request.session['item-in-view']

    hasCart = False
    try:
        if 'cart' in request.session:
            order = Order.objects.get(pk=request.session['cart'])
            hasCart = True
    except:
        print("Either no cart exists or it is invalid")

    return render(request, 'menu-home.html', {'hasCart': hasCart, 'order':order})

# @brief generates the search page
# shows results on word(s) that are in a name/description
#
# @param request The HTTP Request object from the website
# @return a render based on the reqeust, home.html, and a hash which is passed into the html
def SearchPageView(request):
    hasCart = False
    try:
        if 'cart' in request.session:
            order = Order.objects.get(pk=request.session['cart'])
            hasCart = True
    except:
        print("Either no cart exists or it is invalid")
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    drinks = Menu.objects.filter(
        (Q(name__icontains=q) |
        Q(description__icontains=q)) &
        (Q(size__iexact='grande') |
         Q(size__iexact="doppio"))
        
    )
    context = {'drinks': drinks, 'hasCart':hasCart, 'order':order}
    return render(request,'search.html', context)

# @brief generates the page based on the type of drink selected
#
# @param pk The Primary Key for the drink requested 
# @param request The HTTP Request object from the website
# @return a render based on the reqeust, home.html, and a hash which is passed into the html
def DrinksPageView(request,pk):
    order = Order.objects.get(pk=request.session['cart'])
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

    products = Menu.objects.filter(type__iexact=pk, size__iexact="grande")
    return render(request, 'drinks.html', {'products':products, 'hasCart':hasCart, 'name':pk, 'order':order})


def CustomizationDetailView(request, pk):
    order = Order.objects.get(pk=request.session['cart'])
    customizations = Customization.objects.filter(type__iexact=pk)
    return render(request, 'customization.html', {'customizations':customizations, 'name':pk, 'hasCart':True, 'order':order})

# @brief generates the page where the customer can see the drink and can what type of customization to add
#
# @param pk The Primary Key for the drink requested 
# @param request The HTTP Request object from the website
# @return a render based on the reqeust, home.html, and a hash which is passed into the html
def ItemDetailView(request, pk):
    item = Menu.objects.get(pk = pk)
    
    hasCart = False
    try:
        if 'cart' in request.session:
            order1 = Order.objects.get(pk=request.session['cart'])
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
    #     request.session['item-in-view'] = OrderItem.create(
    #             Order.objects.get(pk=order), # Create orderItem belonging to cart
    #             item).pk # Create with menu item selected
    # orderItem = OrderItem.objects.get(pk=request.session['item-in-view'])
    size = 'grande'    
    # If it is a POST request we will process the form data
    if request.method == 'POST':
        # create a form and populate with data from the request
        form = CustomizationForm(request.POST)
        form.setSizes(item.getPossibleSizes())
        # check if the form is valid
        if form.is_valid():
            print(form.cleaned_data)
            order = int(request.session['cart'])
            request.session['item-in-view'] = OrderItem.create(
                Order.objects.get(pk=order), # Create orderItem belonging to cart
                item).pk # Create with menu item selected
            orderItem = OrderItem.objects.get(pk=request.session['item-in-view'])
            size = form.cleaned_data['size']
            print(size)
            item_name  = OrderItem.objects.get(pk=request.session['item-in-view']).menu_item.name
            print(item_name)
            item =  Menu.objects.get(Q(name=item_name) & Q(size=size))
            OrderItem.objects.get(pk=request.session['item-in-view']).delete()
            request.session['item-in-view'] = OrderItem.create(
                Order.objects.get(pk=order), item).pk# Create orderItem belonging to cart
            for key, value in form.cleaned_data.items():
                amount = 1
                if value and value != '':
                    if key[0:3] != 'amt' and key != 'size':
                        if key != 'milk' and key != 'drizzle' and key != 'topping' and key != 'foam' and key != 'lining' and key != 'inclusion':
                            amount_string = 'amt_' + key
                            amount = form.cleaned_data[amount_string]
                        OrderItem.objects.get(pk=request.session['item-in-view']).addCustomization(Customization.objects.get(id=value),amount)
            del request.session['item-in-view']

            return render(request, 'menu-home.html', {'hasCart':hasCart, 'order':order1})
    # If method is GET create a blank form
    else:
        form = CustomizationForm(request.POST)
        form.setSizes(item.getPossibleSizes())

        
    return render(request, 'item-detail.html', {'item': item, 'form':form, 'hasCart':hasCart, 'order':order1})

# @brief generates the location of the stgore on a page
#
# @param request The HTTP Request object from the website
# @return a render based on the reqeust, home.html, and a hash which is passed into the html
def LocationView(request):
    hasCart = False
    try:
        if 'cart' in request.session:
            order = Order.objects.get(pk=request.session['cart'])
            hasCart = True
    except:
        print("Either no cart exists or it is invalid")
    return render(request,'locations.html', {'hasCart': hasCart, 'order':order})

@staff_member_required
def AnalyticsPageView(request):
    return render(request, 'analytics.html', {'hasCart':False})

# @brief generates the page to checkout
#
# @param request The HTTP Request object from the website
# @return a render based on the reqeust, home.html, and a hash which is passed into the html
def CheckoutPageView(request):
    order = Order.objects.get(pk=request.session['cart'])
    # Remove unadded items from cart
    if request.method == 'POST':
        data = request.POST
        if "remove-id" in data:
            item = data.get("remove-id")
            OrderItem.objects.get(id=int(item)).delete()
        elif "checkingout" in data:
            order.checkout()
            del request.session['cart']
            return redirect('home')
      
    return render(request, 'checkout.html', {'order': order, 'hasCart':False})

# @brief generates the page to view the sales report
#
# @param request The HTTP Request object from the website
# @return a render based on the reqeust, home.html, and a hash which is passed into the html
def SalesPageView(request):
    if request.method == 'POST':
        data = request.POST

    return render(request,'analytics/sales.html')

# @brief generates the page to view the excess report
#
# @param request The HTTP Request object from the website
# @return a render based on the reqeust, home.html, and a hash which is passed into the html
def ExcessPageView(request):
    if request.method == 'POST':
        data = request.POST

    return render(request,'analytics/excess.html')

# @brief generates the page to view the frequent report
#
# @param request The HTTP Request object from the website
# @return a render based on the reqeust, home.html, and a hash which is passed into the html
def FrequentPageView(request):
    if request.method == 'POST':
        data = request.POST

    return render(request,'analytics/frequent.html')
# @brief generates the page to view the restock report
#
# @param request The HTTP Request object from the website
# @return a render based on the reqeust, home.html, and a hash which is passed into the html
def RestockPageView(request):
    if request.method == 'POST':
        data = request.POST

    return render(request,'analytics/restock.html')
