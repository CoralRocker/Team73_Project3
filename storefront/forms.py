from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from .models import Customization
from django.forms import MultipleChoiceField, ChoiceField

class CustomizationForm(forms.Form):
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

    size = forms.ChoiceField(required=False, 
                             widget=forms.Select(attrs={
                                                    'value':'Grande',
                                                    'onchange':'submit()',
                                                    'form':'customization_form'})
                             )
    amount = forms.IntegerField(min_value=1, required=False, 
                            widget=forms.NumberInput(attrs={
                                                    'value':1,
                                                    'onchange':'submit()',
                                                    'form':'customization_form'})
                            )

    
    def setSizes(self, sizes):
        self.fields['size']._set_choices(sizes)
        self.fields['size'].initial = 'Grande'
        self.fields['amount'].initial = 1
        
class SplashForm(forms.Form):
    SPLASH_CHOICES = ((item.id, item.name) for item in Customization.objects.filter(type__iexact="splash"))
    splahes = MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=SPLASH_CHOICES, required=False)
    
class MilkForm(forms.Form):
    MILK_CHOICES = ((item.id, item.name) for item in Customization.objects.filter(type__iexact="milk"))
    milk = ChoiceField(label="Milk:", choices=MILK_CHOICES, required=False)
    
class ExtraShotForm(forms.Form):
    Extra_shot = forms.IntegerField(initial=0, min_value=0, max_value=3, required=False)

class SyrupForm(forms.Form):
    Apple_Brown_Sugar = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Apple Brown Sugar:")
    Brown_Sugar = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Brown Sugar:")
    Caramel = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Caramel:")
    Cinnamon_Dolce = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Cinnamon Dolce:")
    Hazelnut = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Hazelnut:")
    Peppermint = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Peppermint:")
    Raspberry = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Raspberry:")
    Toasted_Vanilla = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Toasted Vanilla:")
    Toffee_Nut = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Toffee Nut:")
    Vanilla = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Vanilla:")
    Sugar_Free_Vanilla = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Sugar free Vanilla:")

class SauceForm(forms.Form):
    Mocha = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Mocha:")
    New_Dark_Caramel = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Dark Caramel")
    Pumpkin = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Pumpkin:")
    White_Chocolate_Mocha_Sauce = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="White Chocolate Mocha:")
    
class DrizzleForm(forms.Form):
    DRIZZLE_CHOICES = ((item.id, item.name) for item in Customization.objects.filter(type__iexact="drizzle"))
    drizzles = MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DRIZZLE_CHOICES, required=False)

class LiningForm(forms.Form):
    LINING_CHOICES = ((item.id, item.name) for item in Customization.objects.filter(type__iexact="lining"))
    linings = MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=LINING_CHOICES, required=False)

class ToppingForm(forms.Form):
    TOPPING_CHOICES = ((item.id, item.name) for item in Customization.objects.filter(type__iexact="topping"))
    toppings = MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=TOPPING_CHOICES, required=False)

class MixForm(forms.Form):
    Vanilla_bean_powder = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Vanilla Bean Powder:")
    Chocolate_malt_powder = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Chocolate Malt Powder:")

class FoamForm(forms.Form):
    FOAM_CHOICES = ((item.id, item.name) for item in Customization.objects.filter(type__iexact="foam"))
    foams = MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=FOAM_CHOICES, required=False)

class SweetenerForm(forms.Form):
    Classic_syrup = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Classic Syrup:")
    Liquid_cane_sugar = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Liquid Cane Suagr")
    Honey_blend = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Honey Blend:")


class SweetenerPacketForm(forms.Form):
    Sweet_n_low = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Sweet n Low:")
    Equal = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Equal:")
    Splenda = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Splenda:")
    Stevia_blend = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Stevia Blend:")

class InclusionForm(forms.Form):
    INCLUSION_CHOICES = ((item.id, item.name) for item in Customization.objects.filter(type__iexact="inclusion"))
    inclusions = MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=INCLUSION_CHOICES, required=False)

    
class ChaiForm(forms.Form):
    Chai_pump = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Chai Pump:")

class JuiceForm(forms.Form):
    Apple_juice = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Apple Juice:")
    Peach_juice_blend = forms.IntegerField(initial=0, min_value=0, max_value=12, required=False, label="Peach Juice Blend:")
