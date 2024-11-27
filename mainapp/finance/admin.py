from django.contrib import admin

# Register your models here.from django.contrib import admin
from .models import Customer, Product, Invoice, InvoiceItem, Expense


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_created', 'due_date', 'status')
    inlines = [InvoiceItemInline]


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Expense)
