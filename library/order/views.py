import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order
from book.models import Book
from authentication.decorator import librarian_required
from .forms import OrderCreateForm, OrderCloseForm

def orders_list_view(request):
    """Displaying orders: the librarian sees all, the user only sees their own."""
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to the system.")

        return redirect('login')

    if request.user.role == 1:
        orders = Order.objects.select_related('book', 'user').all().order_by('-created_at')
    else:
        orders = Order.objects.select_related('book').filter(user=request.user).order_by('-created_at')

    return render(request, 'orders_list.html', {'orders': orders})


def create_order_view(request, book_id):
    """Creating a book order by a reader through a custom method Order.create."""
    if not request.user.is_authenticated:

        return redirect('login')

    book = get_object_or_404(Book, id=book_id)
    form = OrderCreateForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        if form.save_order(request.user, book):
            messages.success(request, f"Книгу «{book.name}» успішно замовлено!")
            return redirect('orders_list')
        messages.error(request, "Не вдалося замовити книгу. Усі примірники на руках.")
        return redirect('all_books')

    return render(request, 'create_order.html', {'form': form, 'book': book})


@librarian_required
def close_order_view(request, book_id):
    """Closing an order by a librarian via the order.update model method.""" 
    if not request.user.is_authenticated:
        return redirect('login')

    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.book = book
            if book.count > 0:
                order.save()
                book.count -= 1
                book.save()
                messages.success(request, f"Книгу «{book.name}» успішно замовлено!")
                return redirect('orders_list')
            else:
                messages.error(request, "Не вдалося замовити книгу. Усі примірники на руках.")
                return redirect('all_books')
        else:
            messages.error(request, "Некоректно заповнена дата.")
    else:
        default_date = datetime.datetime.now() + datetime.timedelta(weeks=2)
        initial_date = default_date.strftime('%Y-%m-%dT%H:%M')
        form = OrderCreateForm(initial={'plated_end_at': initial_date})

        return render(request, 'create_order.html', {'form': form, 'book': book})


@librarian_required
def close_order_view(request, order_id):
    """Closing an order by a librarian using Django Forms (PUT/Update method).""" 
    order = get_object_or_404(Order, pk=order_id)
    if order.end_at is not None:
        messages.error(request, "Це замовлення вже було закрите.")

        return redirect('orders_list')
    
    form = OrderCloseForm(request.POST or None, instance=order)

    if request.method == 'POST' and form.is_valid():
        form.close_order()
        messages.success(request, f"Замовлення №{order.id} успішно закрите.")
        return redirect('orders_list')

    return render(request, 'close_order.html', {'form': form, 'order': order})