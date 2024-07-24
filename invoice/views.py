from django.shortcuts import render, redirect
from invoice.models import Invoice, Item
from django.db.models import Sum
# Create your views here.


def home(request):
    context = Invoice.objects.all().order_by("-created_at")
    return render(request, 'base.html', {"context": context})

def invoice_detail(request, id):
    context = Invoice.objects.filter(id=id).first()
    items = context.items.all()
    return render(request, 'create.html', {"context": context, "items": items})


def remove_item(request, invoice_id, id):
    invoice_obj = Invoice.objects.filter(id=invoice_id).first()
    item_obj = Item.objects.filter(id=id).first()
    item_obj.delete()
    invoice_obj.save()
    if not invoice_obj.items.all():
        invoice_obj.delete()
        return redirect('home')
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
        item_obj = Item.objects.create(
            name=request.POST.get('item'),
            quantity=int(request.POST.get('quantity')),
            price_per_quantity = float(request.POST.get('price')),
            total_price_item = float(int(request.POST.get('quantity'))) * float(request.POST.get('price'))
            )
        
        invoice_obj.items.add(item_obj)
        invoice_obj.save()
        total = 0.0
        for each in invoice_obj.items.all():
            total = float(total) + float(each.total_price_item)
        tax = 0.1 * total
        invoice_obj.tax = tax
        invoice_obj.total_price = total + tax
        invoice_obj.save()

    return redirect('invoice_detail', id=invoice_id)
    


