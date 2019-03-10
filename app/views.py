
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "index.jinja2")

def create_order(request):
    render(request, "create_order.jinja2")
