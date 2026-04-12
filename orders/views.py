from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib import messages
from .models import Order, CATERING_PRICES, ADD_ON_PRICES, TAX_RATE
import json
from decimal import Decimal


ADD_ON_LABELS = {
    'chicken_roast': 'Chicken Roast leg/thai',
    'fish_bhona': 'Fish Bhona',
    'beef_rezella': 'Beef Rezella',
    'samee_kebab': 'Samee Kebab',
    'firni_payes': 'Firni/Payes',
}


def order_form(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '').strip()
        address = request.POST.get('address', '').strip()
        contact_number = request.POST.get('contact_number', '').strip()
        email_address = request.POST.get('email_address', '').strip()
        catering_option = request.POST.get('catering_option', '')
        number_of_persons = int(request.POST.get('number_of_persons', 1))
        add_ons = request.POST.getlist('add_ons')
        replace_beef_mutton = request.POST.get('replace_beef_mutton') == 'on'
        other_notes = request.POST.get('other_notes', '').strip()
        service_method = request.POST.get('service_method', '')
        service_other = request.POST.get('service_other', '').strip()
        delivery_instructions = request.POST.get('delivery_instructions', '').strip()

        # Validate required fields
        errors = []
        if not customer_name:
            errors.append('Customer name is required.')
        if not contact_number:
            errors.append('Contact number is required.')
        if not email_address:
            errors.append('Email address is required.')
        if not catering_option:
            errors.append('Please select a catering option.')
        if not service_method:
            errors.append('Please select a method of service.')
        if service_method == 'delivery' and not address:
            errors.append('Address is required for delivery orders.')

        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, 'orders/order_form.html', {'post': request.POST})

        # Calculate pricing
        base_price = Decimal(str(CATERING_PRICES.get(catering_option, 0)))
        addon_total = Decimal('0')
        for addon in add_ons:
            addon_total += Decimal(str(ADD_ON_PRICES.get(addon, 0)))

        if replace_beef_mutton:
            addon_total += Decimal('1.00')

        per_person = base_price + addon_total
        subtotal = per_person * number_of_persons
        tax_amount = subtotal * Decimal(str(TAX_RATE))
        total = subtotal + tax_amount

        order = Order.objects.create(
            customer_name=customer_name,
            address=address,
            contact_number=contact_number,
            email_address=email_address,
            catering_option=catering_option,
            number_of_persons=number_of_persons,
            add_ons=add_ons,
            replace_beef_mutton=replace_beef_mutton,
            other_notes=other_notes,
            service_method=service_method,
            service_other=service_other,
            delivery_instructions=delivery_instructions,
            subtotal=subtotal,
            tax_amount=tax_amount,
            total=total,
        )

        # Send email notification
        addon_str = ', '.join([ADD_ON_LABELS.get(a, a) for a in add_ons]) if add_ons else 'None'
        catering_label = dict(Order._meta.get_field('catering_option').choices).get(catering_option, catering_option)
        service_label = dict(Order._meta.get_field('service_method').choices).get(service_method, service_method)

        email_body = f"""
NEW ORDER RECEIVED - Curry King & Grills
==========================================
Order #: {order.id}
Date/Time: {order.created_at.strftime('%Y-%m-%d %H:%M')}

CUSTOMER DETAILS
----------------
Name: {customer_name}
Contact: {contact_number}
Email: {email_address}
Address: {address if address else 'N/A'}

ORDER DETAILS
-------------
Catering Option: {catering_label}
Number of Persons: {number_of_persons}
Add-ons: {addon_str}
Replace Beef with Mutton (+$1): {'Yes' if replace_beef_mutton else 'No'}
Other Notes: {other_notes if other_notes else 'None'}

SERVICE
-------
Method: {service_label}
{('Service Notes: ' + service_other) if service_other else ''}
Delivery Instructions: {delivery_instructions if delivery_instructions else 'None'}

PRICING
-------
Subtotal: ${subtotal:.2f}
Tax (13%): ${tax_amount:.2f}
TOTAL: ${total:.2f}

==========================================
Please confirm payment of min 30% via interac to greenmaple.com@gmail.com
or call Ph# 416 261 0888 / Mob# 437 345 6722
"""
        try:
            send_mail(
                subject=f'[New Order #{order.id}] {customer_name} - ${total:.2f}',
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.KITCHEN_EMAIL],
                fail_silently=False,
            )
            # Send confirmation to customer
            send_mail(
                subject=f'Order Confirmation #{order.id} – Curry King & Grills',
                message=f"""Dear {customer_name},

Thank you for your order at Curry King & Grills!

Your Order #{order.id} has been received. Here's a summary:

{catering_label}
Persons: {number_of_persons}
Add-ons: {addon_str}

Subtotal: ${subtotal:.2f}
Tax (13%): ${tax_amount:.2f}
TOTAL: ${total:.2f}

To finalize your order, please send minimum 30% payment via Interac to greenmaple.com@gmail.com
or call us at Ph# 416 261 0888 / Mob# 437 345 6722.

Thank you for choosing Curry King & Grills!
3541 Saint Clair Ave East, M1K 1L6
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email_address],
                fail_silently=True,
            )
        except Exception as e:
            pass  # Don't fail the order if email fails

        return redirect('order_success', pk=order.pk)

    return render(request, 'orders/order_form.html', {})


def order_success(request, pk):
    order = Order.objects.get(pk=pk)
    catering_label = dict(Order._meta.get_field('catering_option').choices).get(order.catering_option, order.catering_option)
    service_label = dict(Order._meta.get_field('service_method').choices).get(order.service_method, order.service_method)
    addon_labels = {
        'chicken_roast': 'Chicken Roast leg/thai (+$3.50)',
        'fish_bhona': 'Fish Bhona (+$4.00)',
        'beef_rezella': 'Beef Rezella (+$5.00)',
        'samee_kebab': 'Samee Kebab (+$2.00)',
        'firni_payes': 'Firni/Payes (+$2.00)',
    }
    addons = [addon_labels.get(a, a) for a in (order.add_ons or [])]
    return render(request, 'orders/order_success.html', {
        'order': order,
        'catering_label': catering_label,
        'service_label': service_label,
        'addons': addons,
    })
