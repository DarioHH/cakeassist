from datetime import timezone

from django.http import HttpResponseRedirect
from django.shortcuts import render
from app.forms import  OrderForm, ItemFormSet
from django.views.generic.edit import CreateView, UpdateView
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from app.models import Order


def index(request):
    return render(request, "layout.html")

class CreateOrder(CreateView):
    model = Order

    template_name = 'templates/create_order.jinja2'
    form_class = OrderForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(CreateOrder, self).get_context_data(**kwargs)
        if self.request.POST:
            data['orders'] = ItemFormSet(self.request.POST)
        else:
            data['orders'] = ItemFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orders = context['orders']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if orders.is_valid():
                orders.instance = self.object
                orders.save()
        return super(CreateOrder, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('app:order_detail', kwargs={'pk': self.object.pk})

    #     form = OrderFormSet()
    #     form.user = request.user
    #     return render(request, "create_order.jinja2", {'form': form})

# def get_context_data(self, **kwargs):
#     data = super(CollectionUpdate, self).get_context_data(**kwargs)
#     if self.request.POST:
#         data['orders'] = ItemFormSet(self.request.POST, instance=self.object)
#     else:
#         data['orders'] = ItemFormSet(instance=self.object)
#     return data