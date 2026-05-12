from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm
from .models import Category


CATEGORY_SORT_FIELDS = {
    'name': 'name',
    'created': 'created_at',
    'books': 'book_count',
}


@login_required
def category_list(request):
    categories = Category.objects.filter(created_by=request.user).annotate(book_count=Count('books'))

    search = request.GET.get('search', '').strip()
    sort = request.GET.get('sort', 'name')
    direction = request.GET.get('direction', 'asc')

    if search:
        categories = categories.filter(name__icontains=search)

    sort_field = CATEGORY_SORT_FIELDS.get(sort, 'name')
    if direction == 'desc':
        sort_field = f'-{sort_field}'
    categories = categories.order_by(sort_field)

    paginator = Paginator(categories, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    query_params = request.GET.copy()
    query_params.pop('page', None)

    return render(request, 'categories/category_list.html', {
        'page_obj': page_obj,
        'search': search,
        'sort': sort,
        'direction': direction,
        'querystring': query_params.urlencode(),
    })


@login_required
def category_create(request):
    form = CategoryForm(request.POST or None, user=request.user)

    if request.method == 'POST' and form.is_valid():
        category = form.save(commit=False)
        category.created_by = request.user
        category.save()
        messages.success(request, 'Category added successfully.')
        return redirect('category_list')

    return render(request, 'categories/category_form.html', {
        'form': form,
        'title': 'Add Category',
        'submit_label': 'Add Category',
    })


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk, created_by=request.user)
    form = CategoryForm(request.POST or None, instance=category, user=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Category updated successfully.')
        return redirect('category_list')

    return render(request, 'categories/category_form.html', {
        'form': form,
        'title': 'Edit Category',
        'submit_label': 'Save Changes',
    })


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, created_by=request.user)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category_list')

    return render(request, 'categories/category_confirm_delete.html', {'category': category})
