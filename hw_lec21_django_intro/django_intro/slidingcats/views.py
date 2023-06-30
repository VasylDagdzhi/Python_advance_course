from django.shortcuts import render
from django.http import HttpResponse
from .models import MenuItem, Slider


# Create your views here.
def index(request):
    return render(request, "index.html", {"menu_items": MenuItem.objects.all(), "sliders": Slider.objects.all()})
