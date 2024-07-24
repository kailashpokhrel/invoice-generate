from django.shortcuts import render, redirect
from invoice.models import Invoice, Item

def home(request):
    context = Invoice.objects.all().order_by("-created_at")
    return render(request, 'base.html', {"context": context})

def invoice_detail(request, id):
    context = Invoice.objects.filter(id=id).first()
    items = context.items.all()
    return render(request, 'create.html', {"context": context, "items": items})

def remove_invoice(request, id):
    context = Invoice.objects.filter(id=id).first()
    items = context.items.all()
    
    return render(request, 'create.html', {"context": context, "items": items})

def remove_item(request, invoice_id, id):
    # Retrieve the invoice and item objects
    invoice_obj = Invoice.objects.filter(id=invoice_id).first()
    item_obj = Item.objects.filter(id=id).first()

    # Delete the item
    if item_obj:
        item_obj.delete()
        item_obj.save()
        
   
    if not invoice_obj.items.all():
        invoice_obj.delete()
        return redirect('home')
    
    # Recalculate totals and tax
    total = 0.0
    for each in invoice_obj.items.all():
        total = float(total) + float(each.total_price_item)
    tax = 0.1 * total
    invoice_obj.tax = tax
    invoice_obj.total_price = total + tax
    invoice_obj.save()

    return redirect('invoice_detail', id=invoice_id)

def add_invoice(request):
    invoice_obj = Invoice.objects.create(tax=0, total_price=0)
    return redirect('invoice_detail', id=invoice_obj.id)

def add_item(request, invoice_id):
    if request.method == "POST" :
        invoice_obj = Invoice.objects.filter(id=invoice_id).first()

        # Convert POST data to Decimal
        item_name = request.POST.get('item')
        quantity = float(request.POST.get('quantity'))
        price_per_quantity = float(request.POST.get('price'))
        total_price_item = quantity * price_per_quantity

        # Create new item
        item_obj = Item.objects.create(
            name=item_name,
            quantity=quantity,
            price_per_quantity=price_per_quantity,
            total_price_item=total_price_item
        )

        # Add item to invoice
        if item_obj:
            invoice_obj.items.add(item_obj)
            invoice_obj.save()

        # Update invoice totals
        total = 0.0
        for each in invoice_obj.items.all():
            total = float(total) + float(each.total_price_item)

        tax = 0.1 * total
        invoice_obj.tax = tax
        invoice_obj.total_price = total + tax

        invoice_obj.save()

    return redirect('invoice_detail', id=invoice_id)
    

