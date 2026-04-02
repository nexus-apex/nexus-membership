from django.db import models

class MemberProfile(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=255, blank=True, default="")
    plan_name = models.CharField(max_length=255, blank=True, default="")
    join_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("expired", "Expired"), ("suspended", "Suspended"), ("cancelled", "Cancelled")], default="active")
    auto_renew = models.BooleanField(default=False)
    total_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class MembershipPlan(models.Model):
    name = models.CharField(max_length=255)
    duration = models.CharField(max_length=50, choices=[("monthly", "Monthly"), ("quarterly", "Quarterly"), ("annual", "Annual"), ("lifetime", "Lifetime")], default="monthly")
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    features = models.TextField(blank=True, default="")
    members = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("deprecated", "Deprecated")], default="active")
    trial_days = models.IntegerField(default=0)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class MemberPayment(models.Model):
    member_name = models.CharField(max_length=255)
    plan_name = models.CharField(max_length=255, blank=True, default="")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_date = models.DateField(null=True, blank=True)
    method = models.CharField(max_length=50, choices=[("card", "Card"), ("upi", "UPI"), ("bank", "Bank"), ("cash", "Cash")], default="card")
    status = models.CharField(max_length=50, choices=[("paid", "Paid"), ("failed", "Failed"), ("refunded", "Refunded")], default="paid")
    next_due = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.member_name
