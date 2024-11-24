from django import forms
from .models import Order, Product, Topping
from datetime import date
from decimal import Decimal

class OrderForm(forms.ModelForm):
    
    # Define form fields
    cake_size_kg = forms.ChoiceField(choices=[(Decimal("1.0"), "1KG"), (Decimal("1.5"), "1.5KG"), (Decimal("2.0"), "2KG")],
    required=True,
    label="Cake Size (Kg)")
    toppings = forms.ModelMultipleChoiceField(
        queryset=Topping.objects.none(),  # Default queryset
        widget=forms.CheckboxSelectMultiple,
        required=False  # Allow no toppings to be selected
    )

    class Meta:
        model = Order
        fields = ['cake_size_kg', 'occasion', 'preferred_colors', 'toppings', 'delivery_date']
        widgets = {
            'delivery_date': forms.DateInput(attrs={'class': 'flatpickr', 'readonly': 'true'}),
        }

    def __init__(self, *args, **kwargs):
        # Get product instance from kwargs
        product = kwargs.pop('product', None)
        print(f"Product in OrderForm: {product}")  # Debugging line
        super().__init__(*args, **kwargs)

        # Dynamically filter toppings based on the product
        if product:
            self.fields['toppings'].queryset = product.toppings.all()
def clean_cake_size_kg(self):
    value = self.cleaned_data['cake_size_kg']
    try:
        return Decimal(value)
    except InvalidOperation:
        raise forms.ValidationError("Invalid cake size value.")
