from django.shortcuts import render, redirect

from items.models import Category, Item

from .forms import SigupForm

# Create your views here.

def index(request):
    items = Item.objects.filter(is_sold = True)[0:6]
    categories = Category.objects.all()
    return render(request, 'corefolder/index.html', {'items': items, 'categories': categories})

def contact(request):
    return render(request, 'corefolder/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SigupForm(request.POST)
        if form.is_valid():
            form.saved()
        
        return redirect('/login/')
    form = SigupForm()


    return render(request, 'corefolder/signup.html', {'form':form})

