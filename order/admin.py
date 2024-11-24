from django.contrib import admin
from django.urls import path, include
from .models import *

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price')  # Columns to display in the admin list
    search_fields = ('name', 'category')              # Searchable fields
    filter_horizontal = ('toppings',)  # Allows easy selection of toppings
    list_editable = ('base_price',)  # Allow editing of base price in the admin list
    list_per_page = 10  # Number of items to display per page

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'delivery_date', 'cake_size_kg', 'occasion', 'preferred_colors', 'toppings','is_paid')  # Columns to display
    list_filter = ('is_paid', 'delivery_date')  # Add filters for these fields
    search_fields = ('user__username', 'product__name')  # Searchable fields
    date_hierarchy = 'delivery_date'  # Display a date hierarchy in the admin list

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')  # Columns to display in the admin list
    list_editable = ('price',)  # Allow editing of price in the admin list