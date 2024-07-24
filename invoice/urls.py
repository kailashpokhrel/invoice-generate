from django.urls import path
from invoice.views import home ,invoice_detail, remove_item, add_invoice, add_item
urlpatterns = [
   path("", home, name="home"),
   path("invoice-detail/<int:id>/", invoice_detail, name="invoice_detail"),
   path("remove-invoice/<int:invoice_id>/<int:id>/",remove_item, name="remove_item" ),
   path("add-invoice/", add_invoice, name="add_invoice"),
   path("add-item/<int:invoice_id>/", add_item, name="add_item")
]