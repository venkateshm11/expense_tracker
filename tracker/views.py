from django.shortcuts import redirect, render
from django.db.models import Sum
from tracker.models import Transaction

# Create your views here.
def index(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        amount = float(request.POST.get('amount'))

        if not description or amount == 0:
            return redirect('index')

        transaction = Transaction(
            description=description,
            amount=amount
        )

        transaction.save()
        return redirect('index')
        
    
    transactions = Transaction.objects.all().order_by('-date')

    income = Transaction.objects.filter(amount__gt=0).aggregate(total=Sum('amount'))['total'] or 0
    expenses = Transaction.objects.filter(amount__lt=0).aggregate(total=Sum('amount'))['total'] or 0
    balance = income + expenses 

    context = {
        'transactions': transactions,
        'income': income,
        'expenses': expenses,
        'balance': balance
    }

        
    return render(request, 'index.html', context)

def delete_transaction(request, id):
    transaction = Transaction.objects.get(id=id)
    transaction.delete()
    return redirect('index')