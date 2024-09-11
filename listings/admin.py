from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, ProductImage
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', ] 


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']