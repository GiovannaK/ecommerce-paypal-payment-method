from django.contrib import admin
from . import models


class VariationInline(admin.TabularInline):
    model = models.Variation
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_formated_price']
    inlines = [
        VariationInline
    ]
    readonly_fields = ["slug"]

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 1    


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ["slug"]

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Variation)
admin.site.register(models.Profile)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem)