import django_filters
from django.forms import ModelForm, BaseFormSet
from django import forms
from app.models import Order, Item
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
from datetime import datetime, timedelta


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

    def cleaned_data(self):
        cake = self.cleaned_data['cake']
        if cake == '':
            raise forms.ValidationError("Cake empty")
        return cake

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity == '':
            raise forms.ValidationError("quantity invalid")
        return quantity

    def get(self):
        return self

class DateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, *args, **kwargs):
        super(DateInput, self).__init__(*args, **kwargs)

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_day', 'shop']
        exclude = ['created_by', ]
        widgets = {
            'delivery_day': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        today = datetime.now()
        new_date = today + timedelta(days=1)
        self.fields["delivery_day"].initial = new_date
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('shop'),
                Field('delivery_day', value=new_date.strftime('%d/%m/%Y'), text=new_date.strftime('%d/%m/%Y')   ),
                Fieldset('Add item',
                         Formset('order')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
            )
        )

class OrderDetailsFormSet(BaseFormSet):

    def clean(self):
        if any(self.errors):
            print('bad error')
        return
        cakes = []
        for form in self.forms:
            cake = form.cleaned_data['cake']
            quantity = form.cleaned_data['quantity']
            if int(quantity) <= 0:
                raise forms.ValidationError('the quantity should be > 0')
            if cake in cakes:
                raise forms.ValidationError('Cake in a set must have distinct')

class OrderFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Order
        fields = ['shop', 'delivery_day']

class DateOrderForm(forms.Form):

    def __init__(self, choices, selected):
        super(DateOrderForm, self).__init__()
        self.fields['select'] = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'data-delivery-day': None, 'selected': selected.strftime("%Y-%m-%d")}))


ItemFormSet = inlineformset_factory(
    Order, Item, form=ItemForm, fields=('cake', 'quantity'), extra=1, can_delete=True,formset=OrderDetailsFormSet)

