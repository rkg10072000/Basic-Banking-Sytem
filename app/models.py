from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=255)
    balance = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TransferHistory(models.Model):
    sender = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='transfer_history')
    receiver = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='tranfer_history')
    amount = models.FloatField()

    def __str__(self):
        return f'{self.sender} sent {self.amount}rs to {self.receiver}'