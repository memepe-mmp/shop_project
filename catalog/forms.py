from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "title", "description", "price",
            "status", "category", "author", "characteristics",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "charactetistics": forms.SelectMultiple(attrs={"size": 6}),
        }