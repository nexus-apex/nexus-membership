from django.contrib import admin
from .models import MemberProfile, MembershipPlan, MemberPayment

@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "plan_name", "join_date", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "email", "phone"]

@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ["name", "duration", "price", "members", "status", "created_at"]
    list_filter = ["duration", "status"]
    search_fields = ["name"]

@admin.register(MemberPayment)
class MemberPaymentAdmin(admin.ModelAdmin):
    list_display = ["member_name", "plan_name", "amount", "payment_date", "method", "created_at"]
    list_filter = ["method", "status"]
    search_fields = ["member_name", "plan_name"]
