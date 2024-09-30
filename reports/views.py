from django.shortcuts import render
from operation.models import PurchaseDetails,SaleDetails
from master.models import Item
from django.db.models import Sum

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
