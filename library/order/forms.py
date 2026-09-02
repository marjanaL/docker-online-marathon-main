import datetime
from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['plated_end_at']
        labels = {'plated_end_at': 'Планована дата повернення:'}
        widgets = {'plated_end_at': forms.DateTimeInput(attrs={'type': 'datetime-local'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.initial.get('plated_end_at'):
            future_date = datetime.datetime.now() + datetime.timedelta(weeks=2)
            self.initial['plated_end_at'] = future_date.strftime('%Y-%m-%dT%H:%M')

    def save_order(self, user, book):
        order = self.save(commit=False)
        order.user = user
        order.book = book
        
        if book.count > 0:
            order.save()
            book.count -= 1
            book.save()
            return order
        return None


class OrderCloseForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['end_at']
        labels = {'end_at': 'Фактична дата повернення книги:'}
        widgets = {'end_at': forms.DateTimeInput(attrs={'type': 'datetime-local'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')
        self.initial['end_at'] = current_time

    def close_order(self):
        order = self.save()
        if order.book:
            order.book.count += 1
            order.book.save()
        return order
