from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from .models import Customization

class EspressoCustomizationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('size', css_class='form-group col-md-6 mb-0'),
                Column('milk', css_class='form-group col-md-6 mb-0'),
                Column('syrup', 'amt_syrup', css_class='form-group col-md-6 mb-0'),
                Column('sauce', 'amt_sauce', css_class='form-group col-md-6 mb-0'),
                Column('drizzle', css_class='form-group col-md-6 mb-0'),
                Column('lining',css_class='form-group col-md-6 mb-0'),
                Column('topping', css_class='form-group col-md-6 mb-0'),
                Column('mix', 'amt_mix', css_class='form-group col-md-6 mb-0'),
                Column('foam', css_class='form-group col-md-6 mb-0'),
                Column('sweetener', 'amt_sweetener', css_class='form-group col-md-6 mb-0'),
                Column('sweetener_packet', 'amt_sweetener_packet', css_class='form-group col-md-6 mb-0'),
                Column('inclusion', css_class='form-group col-md-6 mb-0'),
                Column('chai', 'amt_chai', css_class='form-group col-md-6 mb-0'),
                Column('juice', 'amt_juice', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )

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

    size = forms.ChoiceField(required=True, choices=[("Solo","Solo"),("Doppio","Doppio"),("Triple","Triple"),("Quad","Quad")], initial='Doppio')

    milk = forms.ChoiceField(required=False, choices=cust_milk, initial='')

    splash = forms.ChoiceField(required=False, choices=cust_splash, initial='')
    syrup = forms.ChoiceField(required=False, choices=cust_syrups, initial='')
    amt_syrup = forms.IntegerField(min_value=0, max_value=12, required=False)
    sauce = forms.ChoiceField(required=False, choices=cust_sauces, initial='')
    amt_sauce = forms.IntegerField(min_value=0, max_value=12, required=False)
    drizzle = forms.ChoiceField(required=False, choices=cust_drizzle, initial='')
    lining = forms.ChoiceField(required=False, choices=cust_lining, initial='')
    topping = forms.ChoiceField(required=False, choices=cust_topping, initial='')
    mix = forms.ChoiceField(required=False, choices=cust_mix, initial='')
    amt_mix = forms.IntegerField(min_value=0, max_value=12, required=False)
    foam = forms.ChoiceField(required=False, choices=cust_foam, initial='')
    sweetener = forms.ChoiceField(required=False, choices=cust_sweetener, initial='')
    amt_sweetener = forms.IntegerField(min_value=0, max_value=12, required=False)
    sweetener_packet = forms.ChoiceField(required=False, choices=cust_sweetener_packet, initial='')
    amt_sweetener_packet = forms.IntegerField(min_value=0, max_value=12, required=False)
    inclusion = forms.ChoiceField(required=False, choices=cust_inclusion, initial='')
    chai = forms.ChoiceField(required=False, choices=cust_chai, initial='')
    amt_chai = forms.IntegerField(min_value=0, max_value=12, required=False)
    juice = forms.ChoiceField(required=False, choices=cust_juice, initial='')
    amt_juice = forms.IntegerField(min_value=0, max_value=12, required=False)
    


class ElseCustomizationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Column('size', css_class='form-group col-md-6 mb-0'),
                Column('milk', css_class='form-group col-md-6 mb-0'),
                Column('syrup', 'amt_syrup', css_class='form-group col-md-6 mb-0'),
                Column('sauce', 'amt_sauce', css_class='form-group col-md-6 mb-0'),
                Column('drizzle', css_class='form-group col-md-6 mb-0'),
                Column('lining',css_class='form-group col-md-6 mb-0'),
                Column('topping', css_class='form-group col-md-6 mb-0'),
                Column('mix', 'amt_mix', css_class='form-group col-md-6 mb-0'),
                Column('foam', css_class='form-group col-md-6 mb-0'),
                Column('sweetener', 'amt_sweetener', css_class='form-group col-md-6 mb-0'),
                Column('sweetener_packet', 'amt_sweetener_packet', css_class='form-group col-md-6 mb-0'),
                Column('inclusion', css_class='form-group col-md-6 mb-0'),
                Column('chai', 'amt_chai', css_class='form-group col-md-6 mb-0'),
                Column('juice', 'amt_juice', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )

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

    size = forms.ChoiceField(required=True, choices=[("Short","Short"),("Tall","Tall"),("Grande","Grande"),("Venti","Venti"),("Trenta","Trenta")], initial='Grande')

    milk = forms.ChoiceField(required=False, choices=cust_milk, initial='')

    splash = forms.ChoiceField(required=False, choices=cust_splash, initial='')
    syrup = forms.ChoiceField(required=False, choices=cust_syrups, initial='')
    amt_syrup = forms.IntegerField(min_value=0, max_value=12, required=False)
    sauce = forms.ChoiceField(required=False, choices=cust_sauces, initial='')
    amt_sauce = forms.IntegerField(min_value=0, max_value=12, required=False)
    drizzle = forms.ChoiceField(required=False, choices=cust_drizzle, initial='')
    lining = forms.ChoiceField(required=False, choices=cust_lining, initial='')
    topping = forms.ChoiceField(required=False, choices=cust_topping, initial='')
    mix = forms.ChoiceField(required=False, choices=cust_mix, initial='')
    amt_mix = forms.IntegerField(min_value=0, max_value=12, required=False)
    foam = forms.ChoiceField(required=False, choices=cust_foam, initial='')
    sweetener = forms.ChoiceField(required=False, choices=cust_sweetener, initial='')
    amt_sweetener = forms.IntegerField(min_value=0, max_value=12, required=False)
    sweetener_packet = forms.ChoiceField(required=False, choices=cust_sweetener_packet, initial='')
    amt_sweetener_packet = forms.IntegerField(min_value=0, max_value=12, required=False)
    inclusion = forms.ChoiceField(required=False, choices=cust_inclusion, initial='')
    chai = forms.ChoiceField(required=False, choices=cust_chai, initial='')
    amt_chai = forms.IntegerField(min_value=0, max_value=12, required=False)
    juice = forms.ChoiceField(required=False, choices=cust_juice, initial='')
    amt_juice = forms.IntegerField(min_value=0, max_value=12, required=False)
    

