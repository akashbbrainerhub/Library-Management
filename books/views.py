from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from categories.models import Category
from .forms import BookForm
from .models import Book


BOOK_SORT_FIELDS = {
    'title': 'title',
    'author': 'author',
    'category': 'category__name',
    'created': 'created_at',
}



def book_list(request):
    books = Book.objects.filter(created_by=request.user).select_related('category', 'created_by')
    categories = Category.objects.filter(created_by=request.user)

    search = request.GET.get('search', '').strip()
    category_id = request.GET.get('category', '').strip()
    sort = request.GET.get('sort', 'created')
    direction = request.GET.get('direction', 'desc')

    if search:
        books = books.filter(
            Q(title__icontains=search)
            | Q(author__icontains=search)
            | Q(isbn__icontains=search)
            | Q(description__icontains=search)
        )

    if category_id:
        books = books.filter(category_id=category_id)

    sort_field = BOOK_SORT_FIELDS.get(sort, 'created_at')
    if direction == 'desc':
        sort_field = f'-{sort_field}'
    books = books.order_by(sort_field)

    paginator = Paginator(books, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    query_params = request.GET.copy()
    query_params.pop('page', None)

    return render(request, 'books/book_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'search': search,
        'selected_category': category_id,
        'sort': sort,
        'direction': direction,
        'querystring': query_params.urlencode(),
    })


@login_required
def book_create(request):
    form = BookForm(request.POST or None, user=request.user)

    if request.method == 'POST' and form.is_valid():
        book = form.save(commit=False)
        book.created_by = request.user
        book.save()
        messages.success(request, 'Book added successfully.')
        return redirect('book_list')

    return render(request, 'books/book_form.html', {
        'form': form,
        'title': 'Add Book',
        'submit_label': 'Add Book',
    })


@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk, created_by=request.user)
    form = BookForm(request.POST or None, instance=book, user=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Book updated successfully.')
        return redirect('book_list')

    return render(request, 'books/book_form.html', {
        'form': form,
        'title': 'Edit Book',
        'submit_label': 'Save Changes',
    })


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk, created_by=request.user)

    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully.')
        return redirect('book_list')

    return render(request, 'books/book_confirm_delete.html', {'book': book})
