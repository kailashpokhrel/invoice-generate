from django.contrib import admin
from invoice.models import Invoice, Item

admin.site.register(Invoice)
admin.site.register(Item)