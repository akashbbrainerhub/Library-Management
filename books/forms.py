from django import forms

from categories.models import Category

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'description', 'quantity', 'is_available', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Book title', 'class': 'form-control'}),
            'author': forms.TextInput(attrs={'placeholder': 'Author name', 'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'placeholder': 'ISBN', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Short description', 'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'checkbox-input'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['category'].queryset = Category.objects.filter(created_by=user)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 1:
            raise forms.ValidationError('Quantity must be at least 1.')
        return quantity

    def clean_category(self):
        category = self.cleaned_data['category']
        if category.created_by_id != self.user.id:
            raise forms.ValidationError('Choose one of your own categories.')
        return category
