from datetime import timezone

from django.http import HttpResponseRedirect
from django.shortcuts import render
from app.forms import OrderFormSet

def index(request):
    return render(request, "layout.html")

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            form.user = request.user
            form.created_at = timezone.now()
            return HttpResponseRedirect('list_orders/')
    else:
        form = OrderFormSet()
        form.user = request.user
        return render(request, "create_order.jinja2", {'form': form})
