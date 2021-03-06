from datetime import timezone, datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.handlers.exception import response_for_exception
from django.forms import forms, Select, ChoiceField, RadioSelect, ModelChoiceField
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, render_to_response, redirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth.decorators import user_passes_test
from app.forms import OrderForm, ItemFormSet, OrderFilter, DateOrderForm
from django.views.generic.edit import CreateView, UpdateView
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from app.models import Order, Item

def index(request):
    return render(request, "layout.html")




@method_decorator(login_required, name='dispatch')
class CreateOrder(CreateView):
    template_name = 'templates/create_order.jinja2'
    form_class = OrderForm
    model = Order
    success_url = reverse_lazy('order_detail')

    def get_context_data(self, **kwargs):
        data = super(CreateOrder, self).get_context_data(**kwargs)
        if self.request.POST:
            data['order'] = ItemFormSet(self.request.POST, self.request.FILES, prefix='items')
        else:
            data['order'] = ItemFormSet(prefix='items')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        order = form.save(commit=False)
        formset = form
        with transaction.atomic():
            order.created_by = self.request.user
            # for item in context['items']:
            #     item.order = order
            #     item.save()
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object

                for item in context['order'].forms:
                    if item.is_valid():
                        item = item.save(commit=False)
                        item.order = order
                        item.save()

            return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
                 return reverse_lazy('order_detail', kwargs={'pk': self.object.pk})

    #     form = OrderFormSet()
    #     form.user = request.user
    #     return render(request, "create_order.jija2", {'form': form})

class OrderDetailView(DetailView):
    model = Order
    template_name = "order_detail.jinja2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.filter(order=self.object)
        return context
# def get_context_data(self, **kwargs):
#     modletdata = super(CollectionUpdate, self).get_context_data(**kwargs)
#     if self.request.POST:
#         data['orders'] = ItemFormSet(self.request.POST, instance=self.object)
#     else:
#         data['orders'] = ItemFormSet(instance=self.object)
#     return data

@method_decorator(login_required, name='dispatch')
class listYourOrders(ListView):
    model = Order
    template_name = "your_order.jinja2"
    paginate_by = 10
    
    def get_queryset(self):
        """Return the last five published questions."""
        return Order.objects.filter(created_by=self.request.user)


def is_baker(user):
    return user.profile.baker


@login_required
@user_passes_test(is_baker)
def order_by_shop_view(request):
    orders = {}
    for order in Order.objects.all():
        if order.delivery_day_to_str in orders:
            orders[order.delivery_day_to_str].append(order)
        else:
            orders[order.delivery_day_to_str] = [order]
    today = datetime.today()
    form = DateOrderForm(choices=((day, day) for day in orders), selected=today)
    # form = ChoiceField(choices=list(map(tuple, zip(orders.keys(), orders.keys()))))

    return render(request, 'order_by_shop.html', {'orders': orders, 'form': form})

