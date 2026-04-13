from django.db import models

CATERING_OPTIONS = [
    ('premium_14_99', '$14.99/person – Polau, Chicken Roast leg/thai, Fish Bhona, Beef Rezella, Kebab, Firni/Payes'),
    ('standard_10_99', '$10.99/person – Polau, Chicken Roast leg/thai, Fish Bhona, Kebab, Firni/Payes'),
    ('basic_7_99', '$7.99/person – Polau, Chicken Roast leg/thai, Kebab, Firni/Payes'),
    ('wrap_5_99', '$5.99/person – Shawarma Chicken Wrap with Naan'),
    ('biryani_4_99', '$4.99/person – Chicken Biryani with leg/thai and an egg'),
]

SERVICE_OPTIONS = [
    ('pickup', 'Pick-up (Free of charge)'),
    ('delivery', 'Delivery'),
    ('other', 'Other'),
]

ADD_ON_PRICES = {
    'shawarma_chicken_wrap': 7.99,
    'medium_cheese_pizza': 7.99,
    'chicken_roast': 3.50,
    'fish_bhona': 4.00,
    'beef_rezella': 5.00,
    'samee_kebab': 2.00,
    'firni_payes': 1.50,
    'gulab_jam': 1.00,
    'veg_samosa': 0.75,
    'bbq_chicken': 3.00,
    'jorda': 1.50,
    'sutki_dry_fish': 3.00,
    'mix_vegetable': 5.00,
    'chinese_vegetable': 5.00,
    'bhona_khichuri': 5.00,
    'karala_bhaji': 5.00,
    'bindi_bhaji': 5.00,
    'italian_pasta': 8.99,
}

CATERING_PRICES = {
    'premium_14_99': 14.99,
    'standard_10_99': 10.99,
    'basic_7_99': 7.99,
    'wrap_5_99': 5.99,
    'biryani_4_99': 4.99,
}

TAX_RATE = 0.13


class Order(models.Model):
    customer_name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    contact_number = models.CharField(max_length=50)
    email_address = models.EmailField()
    catering_option = models.CharField(max_length=50, choices=CATERING_OPTIONS)
    number_of_persons = models.PositiveIntegerField(default=1)
    add_ons = models.JSONField(default=list, blank=True)
    replace_beef_mutton = models.BooleanField(default=False)
    other_notes = models.TextField(blank=True)
    service_method = models.CharField(max_length=20, choices=SERVICE_OPTIONS)
    service_other = models.CharField(max_length=200, blank=True)
    delivery_instructions = models.TextField(blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"
