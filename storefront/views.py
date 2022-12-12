""" this is the page that generates what is seen"""

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from datetime import date

from .models import *
from .forms import CustomizationForm, SplashForm, MilkForm, ExtraShotForm, SyrupForm, SauceForm
from .forms import DrizzleForm, LiningForm, ToppingForm, MixForm, FoamForm, SweetenerForm, SweetenerPacketForm
from .forms import InclusionForm, ChaiForm, JuiceForm  
class MenuPageView(ListView):
    model = Menu
    template_name = "menu.html"

# @brief generates the home page
#
# @param request The HTTP Request object from the website
# @return a render based on the reqeust, home.html, and a hash which is passed into the html
def HomePageView(request):
    hasCart = False
    order = SET_NULL
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
    order = SET_NULL
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
    order = SET_NULL
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
    order = SET_NULL
    if 'item-in-view' in request.session:
        try:
            OrderItem.objects.get(pk=request.session['item-in-view']).delete()
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

    products = Menu.objects.filter(type__iexact=pk, size__iexact="grande")
    return render(request, 'drinks.html', {'products':products, 'hasCart':hasCart, 'name':pk, 'order':order})


def CustomizationDetailView(request, pk):
    order = Order.objects.get(pk=request.session['cart'])
    orderItem = OrderItem.objects.get(pk=request.session['item-in-view'])
    customizations = Customization.objects.filter(type__iexact=pk)
    if pk == 'milk':
        form = MilkForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                for key, value in form.cleaned_data.items():
                    if value and value != '':
                        orderItem.addCustomization(Customization.objects.get(id=value),1)
                return redirect('item-detail', pk=orderItem.menu_item.id)
    elif pk == 'syrup':
        form = SyrupForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                for key, value in form.cleaned_data.items():
                    name = key.replace("_"," ")
                    if value and value != '':
                        orderItem.addCustomization(Customization.objects.filter(Q(name=name) & Q(type='syrup'))[0],float(value))
                return redirect('item-detail', pk=orderItem.menu_item.id)
    elif pk ==  'coffee':
        form = ExtraShotForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                for key, value in form.cleaned_data.items():
                    name = key.replace("_","-")
                    if value and value != '':
                        orderItem.addCustomization(Customization.objects.get(name=name),float(value))
                return redirect('item-detail', pk=orderItem.menu_item.id)
    elif pk == 'sauce':
        form = SauceForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                for key, value in form.cleaned_data.items():
                    name = key.replace("_"," ")
                    if value and value != '':
                        orderItem.addCustomization(Customization.objects.filter(Q(name=name) & Q(type='sauce'))[0],float(value))
                return redirect('item-detail', pk=orderItem.menu_item.id)
    elif pk ==  'drizzle':
        form = DrizzleForm(request.POST)
    elif pk == 'lining':
        form = LiningForm(request.POST)
    elif pk ==  'topping':
        form = ToppingForm(request.POST)
    elif pk == 'mix':
        form = MixForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                for key, value in form.cleaned_data.items():
                    name = key.replace("_","-")
                    if value and value != '':
                        orderItem.addCustomization(Customization.objects.get(name=name),float(value))
                return redirect('item-detail', pk=orderItem.menu_item.id)
    elif pk ==  'foam':
        form = FoamForm(request.POST)
    elif pk == 'sweetener':
        form = SweetenerForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                for key, value in form.cleaned_data.items():
                    name = key.replace("_","-")
                    if value and value != '':
                        orderItem.addCustomization(Customization.objects.get(name=name),float(value))
                return redirect('item-detail', pk=orderItem.menu_item.id)
    elif pk ==  'sweetener-packet':
        form = SweetenerPacketForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                for key, value in form.cleaned_data.items():
                    name = key.replace("_","-")
                    if value and value != '':
                        orderItem.addCustomization(Customization.objects.get(name=name),float(value))
                return redirect('item-detail', pk=orderItem.menu_item.id)
    elif pk == 'inclusion':
        form = InclusionForm(request.POST)
    elif pk ==  'chai':
        form = ChaiForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                for key, value in form.cleaned_data.items():
                    name = key.replace("_","-")
                    if value and value != '':
                        orderItem.addCustomization(Customization.objects.get(name=name),float(value))
                return redirect('item-detail', pk=orderItem.menu_item.id)
    elif pk == 'juice':
        form = JuiceForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                for key, value in form.cleaned_data.items():
                    name = key.replace("_","-")
                    if value and value != '':
                        orderItem.addCustomization(Customization.objects.get(name=name),float(value))
                return redirect('item-detail', pk=orderItem.menu_item.id)
    elif pk == 'splash':
        form = SplashForm(request.POST)
    if request.method == 'POST':
            if form.is_valid():
                for key, value in form.cleaned_data.items():
                    if value and value != '':
                        for val in value:
                            orderItem.addCustomization(Customization.objects.get(id=val),1)
                return redirect('item-detail', pk=orderItem.menu_item.id)
    return render(request, 'customization.html', {'customizations':customizations, 'name':pk, 'hasCart':True, 'order':order, 'form':form})

# @brief generates the page where the customer can see the drink and can what type of customization to add
#
# @param pk The Primary Key for the drink requested 
# @param request The HTTP Request object from the website
# @return a render based on the reqeust, home.html, and a hash which is passed into the html
def ItemDetailView(request, pk):
    
    item = Menu.objects.get(pk = pk)
    item_description = Menu.objects.filter(Q(name=item.name) & Q(size__iexact='grande'))[0].description
    
    order1 = SET_NULL
    hasCart = False
    
    # Create Cart if it doesn't exist
    if 'cart' not in request.session:
        request.session['cart'] = Order.create('user-created').pk
    try:
        if 'cart' in request.session:
            order1 = Order.objects.get(pk=request.session['cart'])
            hasCart = True
    except:
        print("Either no cart exists or it is invalid")

    

    # Create Temporary Item Session
    # Create if item is different than previous, or if doesn't exist
    if 'item-in-view' not in request.session or (obj := OrderItem.objects.filter(pk=request.session['item-in-view']).first()) == None or obj.menu_item.name != item.name:

        # Delete Previous Items
        if 'item-in-view' in request.session and obj != None:
            OrderItem.objects.get(pk=request.session['item-in-view']).delete()

        order = int(request.session['cart'])
        request.session['item-in-view'] = OrderItem.create(# Create orderItem belonging to cart
                item).pk # Create with menu item selected


    orderItem = OrderItem.objects.get(pk=request.session['item-in-view'])
    size = 'grande'    
    # If it is a POST request we will process the form data
    if request.method == 'POST':
        # create a form and populate with data from the request
        form = CustomizationForm(request.POST)
        form.setSizes(item.getPossibleSizes())
        # check if the form is valid
        if form.is_valid():
            order = int(request.session['cart'])
            orderItem.addOrder(Order.objects.get(pk=order))
            size = form.cleaned_data['size']
            item_name = orderItem.menu_item.name
            item = Menu.objects.filter(size=size, name=item_name).first()
            
            orderItem.amount = form.cleaned_data['amount']
            orderItem.menu_item = item 

            orderItem.save()
            
            for key, value in form.cleaned_data.items():
                if value and value != '':
                    if key[0:3] != 'amt' and key != 'size' and key != 'amount':
                        if key != 'milk' and key != 'drizzle' and key != 'topping' and key != 'foam' and key != 'lining' and key != 'inclusion':
                            amount_string = 'amt_' + key
                            amount = form.cleaned_data[amount_string]
                        orderItem.addCustomization(Customization.objects.get(id=value),amount)

            # The submit button was not pressed, this is just an update
            if not request.POST.get('a2c-btn', False):
                return render(request, 'item-detail.html', {'item': item, 'form':form, 'hasCart':hasCart, 'order':order1, 'orderItem':orderItem, 'item_description':item_description})
                

            del request.session['item-in-view']

            return render(request, 'menu-home.html', {'hasCart':hasCart, 'order':order1})
    # If method is GET create a blank form
    else:
        form = CustomizationForm(request.POST)
        form.setSizes(item.getPossibleSizes())

        
    return render(request, 'item-detail.html', {'item': item, 'form':form, 'hasCart':hasCart, 'order':order1, 'orderItem':orderItem,'item_description':item_description})

# @brief generates the location of the stgore on a page
#
# @param request The HTTP Request object from the website
# @return a render based on the reqeust, home.html, and a hash which is passed into the html
def LocationView(request):
    hasCart = False
    order = SET_NULL
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
    report = ""
    if request.method == 'POST':
        data = request.POST
        if "start_date" in data:
            start_date = data.get("start_date")
        if "end_date" in data:
            end_date = data.get("end_date")
        finances = FinanceView(start_date,end_date)
        report = finances.salesByItem()

    return render(request,'analytics/sales.html', {'report':report})

# @brief generates the page to view the excess report
#
# @param request The HTTP Request object from the website
# @return a render based on the reqeust, home.html, and a hash which is passed into the html
def ExcessPageView(request):
    report = ""
    if request.method == 'POST':
        data = request.POST
        if "timestamp" in data:
            start_date = data.get("timestamp")
        pct = float(data.get('pct', 0.1))
        
        end_date = date.today()
        finances = FinanceView(start_date, end_date)
        report = finances.excessReport(pct)

    return render(request,'analytics/excess.html', {'report':report})

# @brief generates the page to view the frequent report
#
# @param request The HTTP Request object from the website
# @return a render based on the reqeust, home.html, and a hash which is passed into the html
def FrequentPageView(request):
    report = ""
    if request.method == 'POST':
        data = request.POST
        if "start_date" in data:
            start_date = data.get("start_date")
        if "end_date" in data:
            end_date = data.get("end_date")
        
        limit = int(data.get('limit_amt', 100))

        finances = FinanceView(start_date,end_date)
        report = finances.sellsTogetherReportSorted(limit=limit)

    return render(request,'analytics/frequent.html', {'report':report})
# @brief generates the page to view the restock report
#
# @param request The HTTP Request object from the website
# @return a render based on the reqeust, home.html, and a hash which is passed into the html
def RestockPageView(request):
    report = ""
    if request.method == 'POST':
        data = request.POST
        limit = int(data.get('limit_amt', 100))
        start_date = "2022-12-10"
        end_date = date.today()

        finances = FinanceView(start_date,end_date)
        report = finances.restockReport(limit)


    return render(request,'analytics/restock.html', {'report':report})
