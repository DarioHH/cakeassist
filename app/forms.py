from django.forms import ModelForm
from app.models import Order, Cake, Item
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

# class OrderForm(ModelForm):
#     class Meta:
#         model = Order
#         fields = ['shop', 'items']
#

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_day', 'shop', 'user']
        exclude = ['created_by', ]

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('Shop'),
                Field('delivery_day', ),
                Fieldset('Add item',
                         Formset('orders')),
                Field('note'),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
            )
        )



ItemFormSet = inlineformset_factory(
    Order, Item, form=ItemForm, fields=('cake', 'quantity'), extra=1, can_delete=True
    )

