from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'catering_option', 'number_of_persons', 'service_method', 'total', 'created_at')
    list_filter = ('service_method', 'catering_option', 'replace_beef_mutton')
    search_fields = ('customer_name', 'email_address', 'contact_number')
    readonly_fields = ('subtotal', 'tax_amount', 'total', 'created_at')
    ordering = ('-created_at',)
