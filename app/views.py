from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from .models import Customer, TransferHistory

# Create your views here.
def index(req):
    return render(req, 'app/index.html')

def customers(req):
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(req, 'app/accounts.html', context)

def history(req):
    transfer_history = TransferHistory.objects.all()
    context = {'history': transfer_history}
    return render(req, 'app/history.html', context)

def customer(req, pk):
    customer = Customer.objects.get(id=pk)
    context = {
        'name': customer.name,
        'email': customer.email,
        'balance': customer.balance,
        'sentTo': TransferHistory.objects.filter(sender=customer.id),
        'receivedFrom': TransferHistory.objects.filter(receiver=customer.id),
        'receivers': Customer.objects.all().exclude(name=customer.name)
        }
    return render(req, 'app/customer.html', context)

def transaction(req):
    print('coming to function')
    if req.method == 'POST':
        print('comming to if statement')
        receiver = req.POST['receiver']
        amount = int(req.POST['amount'])
        
        sender = req.POST['sender']
        sending_customer = Customer.objects.get(name=sender)
        receiving_customer = Customer.objects.get(name=receiver)
        if int(sending_customer.balance) < amount:
            messages.error(req, "you don't have enough balance in your account to make this transactions")
            return redirect('customer', pk=sending_customer.id)
        
        sending_customer.balance -= amount
        receiving_customer.balance += amount
        transaction = TransferHistory(sender=sending_customer, receiver=receiving_customer, amount=amount)

        sending_customer.save()
        receiving_customer.save()
        transaction.save()

        return redirect('customer', pk=sending_customer.id)
        
            

        

