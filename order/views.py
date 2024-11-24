from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, JsonResponse
#from django.utils.timezone import now
from datetime import date, datetime, timedelta
from .models import Product, Order
from .forms import OrderForm
from decimal import Decimal


# Create your views here
def product_list(request):
    classics = Product.objects.filter(category='classic')
    specials = Product.objects.filter(category='special')
    return render(request, 'product_list.html', {'classics': classics, 'specials': specials})

def order_cake(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    print(f"Product for order form: {product.name} (ID: {product.id})")  # Debugging line

    today_date = date.today()

    if request.method == 'POST':
        form = OrderForm(request.POST, product=product)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.product = product

            # Delivery date validation
            delivery_date = form.cleaned_data['delivery_date']
            if isinstance(delivery_date, datetime):
                delivery_date = delivery_date.date()

            if (delivery_date - today_date).days < 1:
                return HttpResponseBadRequest("Delivery date must be at least 24 hours in advance.")

            # Calculate price
            cake_size_kg = form.cleaned_data['cake_size_kg']
            toppings = form.cleaned_data['toppings']

            if cake_size_kg == Decimal("1.0"):
                base_price = product.price_1kg
            elif cake_size_kg == Decimal("1.5"):
                base_price = product.price_1_5kg
            elif cake_size_kg == Decimal("2.0"):
                base_price = product.price_2kg
            else:
                return HttpResponseBadRequest("Invalid weight selected.")

            topping_cost = sum(topping.price for topping in toppings)
            total_price = base_price + topping_cost

            order.price = total_price  # Ensure 'price' field exists in the model
            order.save()
            print(f"Received cake_size_kg: {cake_size_kg}")  # Add this to see the submitted value


            return redirect('payment_', order.id)
        else:
            print(form.errors)  # Debugging: Log form errors
    else:
        form = OrderForm(product=product)

    return render(request, 'order_form.html', {'form': form, 'product': product, 'delivery_date': today_date})

def calculate_price(request):
    """
    Separate view to calculate the final price dynamically via AJAX.
    """
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        cake_size_kg = request.POST.get('cake_size_kg')
        topping_ids = request.POST.getlist('toppings')

        product = get_object_or_404(Product, id=product_id)

        # Determine base price based on weight
        if cake_size_kg == "1KG":
            base_price = product.price_1kg
        elif cake_size_kg == "1.5KG":
            base_price = product.price_1_5kg
        elif cake_size_kg == "2KG":
            base_price = product.price_2kg
        else:
            return JsonResponse({'error': 'Invalid weight selected'}, status=400)

        # Calculate topping cost
        toppings = Topping.objects.filter(id__in=topping_ids)
        topping_cost = sum([topping.price for topping in toppings])

        # Calculate total price
        total_price = base_price + topping_cost

        return JsonResponse({
            'base_price': float(base_price),
            'topping_cost': float(topping_cost),
            'total_price': float(total_price)
        })
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.is_paid = True
        order.save()
        return redirect('order_success', order.id)
    return render(request, 'payment.html', {'order': order})

def admin_order_list(request):
    # Orders sorted by urgency (closest delivery date first)
    orders = Order.objects.all().order_by('delivery_date')
    return render(request, 'admin_order_list.html', {'orders': orders})

def order_success(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        return render(request, 'order_success.html',{'order' : order})
    except Order.DoesNotExist:
        return render(request, 'order_error.html', {'message': 'Order not found'})