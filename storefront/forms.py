from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from .models import Customization

class CustomizationForm(forms.Form):
    
    cust_milk = [(item.id, item.name) for item in Customization.objects.filter(type__iexact="milk")]
    cust_milk.insert(0, ('', ''))
    
    cust_splash = [(item.id, item.name) for item in Customization.objects.filter(type__iexact="splash")]
    cust_splash.insert(0, ('', ''))
    
    cust_syrups = [(item.id, item.name) for item in Customization.objects.filter(type__iexact="syrup")]
    cust_syrups.insert(0, ('', ''))
    
    cust_sauces = [(item.id, item.name) for item in Customization.objects.filter(type__iexact="sauce")]
    cust_sauces.insert(0, ('', ''))
    
    cust_drizzle = [(item.id, item.name) for item in Customization.objects.filter(type__iexact="drizzle")]
    cust_drizzle.insert(0, ('', ''))
    
    cust_lining = [(item.id, item.name) for item in Customization.objects.filter(type__iexact="lining")]
    cust_lining.insert(0, ('', ''))
    
    cust_topping = [(item.id, item.name) for item in Customization.objects.filter(type__iexact="topping")]
    cust_topping.insert(0, ('', ''))
    
    cust_mix = [(item.id, item.name) for item in Customization.objects.filter(type__iexact="mix")]
    cust_mix.insert(0, ('', ''))
    
    cust_foam = [(item.id, item.name) for item in Customization.objects.filter(type__iexact="foam")]
    cust_foam.insert(0, ('', ''))
    
    cust_sweetener = [(item.id, item.name) for item in Customization.objects.filter(type__iexact="sweetener")]
    cust_sweetener.insert(0, ('', ''))
    
    cust_sweetener_packet = [(item.id, item.name) for item in Customization.objects.filter(type__iexact="sweetener-pack")]
    cust_sweetener_packet.insert(0, ('', ''))
    
    cust_inclusion = [(item.id, item.name) for item in Customization.objects.filter(type__iexact="inclusion")]
    cust_inclusion.insert(0, ('', ''))
    
    cust_chai = [(item.id, item.name) for item in Customization.objects.filter(type__iexact="chai")]
    cust_chai.insert(0, ('', ''))
    
    cust_juice = [(item.id, item.name) for item in Customization.objects.filter(type__iexact="juice")]
    cust_juice.insert(0, ('', ''))
    
    milk = forms.ChoiceField(required=False, choices=cust_milk, initial='')
    milk_amt = forms.IntegerField(min_value=0, required=False)

    splash = forms.ChoiceField(required=False, choices=cust_splash, initial='')
    syrup = forms.ChoiceField(required=False, choices=cust_syrups, initial='')
    sauce = forms.ChoiceField(required=False, choices=cust_sauces, initial='')
    drizzle = forms.ChoiceField(required=False, choices=cust_drizzle, initial='')
    lining = forms.ChoiceField(required=False, choices=cust_lining, initial='')
    topping = forms.ChoiceField(required=False, choices=cust_topping, initial='')
    mix = forms.ChoiceField(required=False, choices=cust_mix, initial='')
    foam = forms.ChoiceField(required=False, choices=cust_foam, initial='')
    sweetener = forms.ChoiceField(required=False, choices=cust_sweetener, initial='')
    sweetener_packet = forms.ChoiceField(required=False, choices=cust_sweetener_packet, initial='')
    inclusion = forms.ChoiceField(required=False, choices=cust_inclusion, initial='')
    chai = forms.ChoiceField(required=False, choices=cust_chai, initial='')
    juice = forms.ChoiceField(required=False, choices=cust_juice, initial='')
    



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('milk', 'milk_amt', css_class='form-group col-md-6 mb-0'),
                Column('syrup', css_class='form-group col-md-6 mb-0'),
                Column('sauce', css_class='form-group col-md-6 mb-0'),
                Column('drizzle', css_class='form-group col-md-6 mb-0'),
                Column('lining', css_class='form-group col-md-6 mb-0'),
                Column('topping', css_class='form-group col-md-6 mb-0'),
                Column('mix', css_class='form-group col-md-6 mb-0'),
                Column('foam', css_class='form-group col-md-6 mb-0'),
                Column('sweetener', css_class='form-group col-md-6 mb-0'),
                Column('sweetener_packet', css_class='form-group col-md-6 mb-0'),
                Column('inclusion', css_class='form-group col-md-6 mb-0'),
                Column('chai', css_class='form-group col-md-6 mb-0'),
                Column('juice', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )
