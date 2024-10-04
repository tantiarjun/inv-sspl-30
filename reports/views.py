from django.shortcuts import render
from operation.models import PurchaseDetails,SaleDetails
from master.models import Item
from django.db.models import Sum
from django.db.models import Q
from django.utils.dateparse import parse_date
from datetime import datetime
from django.http import JsonResponse

def stock_list(request):
    # Fetch all items
    items = Item.objects.filter(status=1)

    # Prepare data for each item with total purchased, sold, and available stock
    stock_data = []
    for item in items:
        # Total quantity purchased for the item
        total_purchased = PurchaseDetails.objects.filter(item_id=item.id).aggregate(
            total_purchased=Sum('quantity')
        )['total_purchased'] or 0
        
        
        # Total quantity sold for the item
        total_sold = SaleDetails.objects.filter(item_id=item.id).aggregate(
            total_sold=Sum('quantity')
        )['total_sold'] or 0
        
        # Available stock is purchased quantity - sold quantity
        available_stock = total_purchased - total_sold

        # Add data to stock_data list
        stock_data.append({
            'item_name': item.item_name,
            'total_purchased': total_purchased,
            'total_sold': total_sold,
            'available_stock': available_stock
        })

    # Pass the stock data to the template
    context = {
        'stock_data': stock_data,
    }
    return render(request,'stock-report/stock_list.html',context)


def detailed_report(request):
    items = Item.objects.filter(status=1)
    
    # Get query params
    item_name = request.GET.get('item', '')
    from_date = request.GET.get('fromdate', '1900-01-01')  # Default to earliest date
    to_date = request.GET.get('todate', str(datetime.now().date()))  # Default to current date
    report_type = request.GET.get('type', 'purchase')  # Default to purchase type

    # Convert string to date
    from_date = parse_date(from_date) or datetime.strptime('1900-01-01', '%Y-%m-%d').date()
    to_date = parse_date(to_date) or datetime.now().date()

    stock_data = []

    if report_type == 'purchase':
        # Fetch purchase data
        purchases = PurchaseDetails.objects.filter(datetime__date__range=[from_date, to_date]).order_by('-datetime')

        if item_name:
            purchases = purchases.filter(item_id__item_name__icontains=item_name)

        for purchase in purchases:
            stock_data.append({
                'item_name': purchase.item_id.item_name,  
                'quantity': purchase.quantity,
                'total': purchase.amount,
                'created_at': purchase.datetime,
                'supplier_or_customer': purchase.purchase_master_id.supplier_id.supplier_name
            })

    elif report_type == 'sales':
        # Fetch sales data
        sales = SaleDetails.objects.filter(datetime__date__range=[from_date, to_date]).order_by('-datetime')

        if item_name:
            sales = sales.filter(item_id__item_name__icontains=item_name)

        for sale in sales:
            stock_data.append({
                'item_name': sale.item_id.item_name,
                'quantity': sale.quantity,
                'total': sale.amount,
                'created_at': sale.datetime,
                'supplier_or_customer': sale.sale_master_id.customer_id.supplier_name
            })

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'stock_data': stock_data})

    # Otherwise, render the template normally
    context = {
        'stock_data': stock_data,
        'items': items
    }
    
    # print(stock_data)

    return render(request, 'detailed-report/detailed_report.html', context)


# def detailed_report(request):
#     items = Item.objects.filter(status=1)
#     Purchase_details = PurchaseDetails.objects.filter(status=1)
    
#     context = {
#         'items': items,
#         'Purchase_details': Purchase_details,
#     }
    
#     return render(request,'detailed-report/detailed_report.html',context)
    




































