from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Item, Category
from .forms import NewItemForm, EditItemForm

# Create your views here.

def items(request):
    items = Item.objects.filter(is_sold=True)
    categories = Category.objects.all()

    category_id = request.GET.get("category")
    query = request.GET.get("query", "").strip()

    if category_id and category_id.isdigit():  # only if numeric
        items = items.filter(category_id=int(category_id))
        category_id = int(category_id)
    else:
        category_id = 0  # default value

    if query:
        items = items.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    return render(request, "item/items.html", {
        "items": items,
        "query": query,
        "categories": categories,
        "category_id": category_id,
    })

def detail(request, pk):
    item= get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=True).exclude(pk=pk)[0:3]

    return render(request, 'item/detail.html', {'item': item, 'related_items':related_items})

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('items:detail', pk=item.id)
        else:
            form = NewItemForm()

    form = NewItemForm()

    return render(request, 'item/form.html', {'form': form, 'title': 'New Item'})

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('/dashboard/')


@login_required
def edit(request, pk):

    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('items:detail', pk=item.id)
        else:
            form = EditItemForm()

    form = NewItemForm()

    return render(request, 'item/form.html', {'form': form, 'title': 'Edit Item'})