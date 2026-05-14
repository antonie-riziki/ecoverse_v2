from django.db import models
from decimal import Decimal


# Create your models here.
from django.db import models

class EcoToken(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    token_mint = models.CharField(max_length=100, blank=True, null=True)
    metadata_url = models.URLField(blank=True, null=True)
    bags_url = models.URLField(blank=True, null=True)
    launch_signature = models.CharField(max_length=200, blank=True, null=True)
    is_launched = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)



class RecyclingSubmission(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("verified", "Verified"),
        ("reward_pending", "Reward Pending"),
        ("reward_sent", "Reward Sent"),
        ("rejected", "Rejected"),
    ]

    user_phone = models.CharField(max_length=30)
    user_wallet = models.CharField(max_length=100, blank=True, null=True)
    waste_kg = models.DecimalField(max_digits=10, decimal_places=2)
    reward_amount = models.DecimalField(max_digits=18, decimal_places=6, default=Decimal("0"))
    center_name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending")
    verification_code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(blank=True, null=True)
    reward_signature = models.CharField(max_length=200, blank=True, null=True)
    reward_error = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user_phone} - {self.waste_kg}kg - {self.status}"