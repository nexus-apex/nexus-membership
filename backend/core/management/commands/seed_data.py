from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import MemberProfile, MembershipPlan, MemberPayment
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusMembership with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusmembership.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if MemberProfile.objects.count() == 0:
            for i in range(10):
                MemberProfile.objects.create(
                    name=["Rajesh Kumar","Priya Sharma","Amit Patel","Deepa Nair","Vikram Singh","Ananya Reddy","Suresh Iyer","Meera Joshi","Karthik Rao","Fatima Khan"][i],
                    email=f"demo{i+1}@example.com",
                    phone=f"+91-98765{43210+i}",
                    plan_name=["Rajesh Kumar","Priya Sharma","Amit Patel","Deepa Nair","Vikram Singh","Ananya Reddy","Suresh Iyer","Meera Joshi","Karthik Rao","Fatima Khan"][i],
                    join_date=date.today() - timedelta(days=random.randint(0, 90)),
                    expiry_date=date.today() - timedelta(days=random.randint(0, 90)),
                    status=random.choice(["active", "expired", "suspended", "cancelled"]),
                    auto_renew=random.choice([True, False]),
                    total_paid=round(random.uniform(1000, 50000), 2),
                )
            self.stdout.write(self.style.SUCCESS('10 MemberProfile records created'))

        if MembershipPlan.objects.count() == 0:
            for i in range(10):
                MembershipPlan.objects.create(
                    name=["Rajesh Kumar","Priya Sharma","Amit Patel","Deepa Nair","Vikram Singh","Ananya Reddy","Suresh Iyer","Meera Joshi","Karthik Rao","Fatima Khan"][i],
                    duration=random.choice(["monthly", "quarterly", "annual", "lifetime"]),
                    price=round(random.uniform(1000, 50000), 2),
                    features=f"Sample features for record {i+1}",
                    members=random.randint(1, 100),
                    status=random.choice(["active", "deprecated"]),
                    trial_days=random.randint(1, 100),
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 MembershipPlan records created'))

        if MemberPayment.objects.count() == 0:
            for i in range(10):
                MemberPayment.objects.create(
                    member_name=["Rajesh Kumar","Priya Sharma","Amit Patel","Deepa Nair","Vikram Singh","Ananya Reddy","Suresh Iyer","Meera Joshi","Karthik Rao","Fatima Khan"][i],
                    plan_name=["Rajesh Kumar","Priya Sharma","Amit Patel","Deepa Nair","Vikram Singh","Ananya Reddy","Suresh Iyer","Meera Joshi","Karthik Rao","Fatima Khan"][i],
                    amount=round(random.uniform(1000, 50000), 2),
                    payment_date=date.today() - timedelta(days=random.randint(0, 90)),
                    method=random.choice(["card", "upi", "bank", "cash"]),
                    status=random.choice(["paid", "failed", "refunded"]),
                    next_due=date.today() - timedelta(days=random.randint(0, 90)),
                )
            self.stdout.write(self.style.SUCCESS('10 MemberPayment records created'))
