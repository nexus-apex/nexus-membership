import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import MemberProfile, MembershipPlan, MemberPayment


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['memberprofile_count'] = MemberProfile.objects.count()
    ctx['memberprofile_active'] = MemberProfile.objects.filter(status='active').count()
    ctx['memberprofile_expired'] = MemberProfile.objects.filter(status='expired').count()
    ctx['memberprofile_suspended'] = MemberProfile.objects.filter(status='suspended').count()
    ctx['memberprofile_total_total_paid'] = MemberProfile.objects.aggregate(t=Sum('total_paid'))['t'] or 0
    ctx['membershipplan_count'] = MembershipPlan.objects.count()
    ctx['membershipplan_monthly'] = MembershipPlan.objects.filter(duration='monthly').count()
    ctx['membershipplan_quarterly'] = MembershipPlan.objects.filter(duration='quarterly').count()
    ctx['membershipplan_annual'] = MembershipPlan.objects.filter(duration='annual').count()
    ctx['membershipplan_total_price'] = MembershipPlan.objects.aggregate(t=Sum('price'))['t'] or 0
    ctx['memberpayment_count'] = MemberPayment.objects.count()
    ctx['memberpayment_card'] = MemberPayment.objects.filter(method='card').count()
    ctx['memberpayment_upi'] = MemberPayment.objects.filter(method='upi').count()
    ctx['memberpayment_bank'] = MemberPayment.objects.filter(method='bank').count()
    ctx['memberpayment_total_amount'] = MemberPayment.objects.aggregate(t=Sum('amount'))['t'] or 0
    ctx['recent'] = MemberProfile.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def memberprofile_list(request):
    qs = MemberProfile.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'memberprofile_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def memberprofile_create(request):
    if request.method == 'POST':
        obj = MemberProfile()
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.plan_name = request.POST.get('plan_name', '')
        obj.join_date = request.POST.get('join_date') or None
        obj.expiry_date = request.POST.get('expiry_date') or None
        obj.status = request.POST.get('status', '')
        obj.auto_renew = request.POST.get('auto_renew') == 'on'
        obj.total_paid = request.POST.get('total_paid') or 0
        obj.save()
        return redirect('/memberprofiles/')
    return render(request, 'memberprofile_form.html', {'editing': False})


@login_required
def memberprofile_edit(request, pk):
    obj = get_object_or_404(MemberProfile, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.plan_name = request.POST.get('plan_name', '')
        obj.join_date = request.POST.get('join_date') or None
        obj.expiry_date = request.POST.get('expiry_date') or None
        obj.status = request.POST.get('status', '')
        obj.auto_renew = request.POST.get('auto_renew') == 'on'
        obj.total_paid = request.POST.get('total_paid') or 0
        obj.save()
        return redirect('/memberprofiles/')
    return render(request, 'memberprofile_form.html', {'record': obj, 'editing': True})


@login_required
def memberprofile_delete(request, pk):
    obj = get_object_or_404(MemberProfile, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/memberprofiles/')


@login_required
def membershipplan_list(request):
    qs = MembershipPlan.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(duration=status_filter)
    return render(request, 'membershipplan_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def membershipplan_create(request):
    if request.method == 'POST':
        obj = MembershipPlan()
        obj.name = request.POST.get('name', '')
        obj.duration = request.POST.get('duration', '')
        obj.price = request.POST.get('price') or 0
        obj.features = request.POST.get('features', '')
        obj.members = request.POST.get('members') or 0
        obj.status = request.POST.get('status', '')
        obj.trial_days = request.POST.get('trial_days') or 0
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/membershipplans/')
    return render(request, 'membershipplan_form.html', {'editing': False})


@login_required
def membershipplan_edit(request, pk):
    obj = get_object_or_404(MembershipPlan, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.duration = request.POST.get('duration', '')
        obj.price = request.POST.get('price') or 0
        obj.features = request.POST.get('features', '')
        obj.members = request.POST.get('members') or 0
        obj.status = request.POST.get('status', '')
        obj.trial_days = request.POST.get('trial_days') or 0
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/membershipplans/')
    return render(request, 'membershipplan_form.html', {'record': obj, 'editing': True})


@login_required
def membershipplan_delete(request, pk):
    obj = get_object_or_404(MembershipPlan, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/membershipplans/')


@login_required
def memberpayment_list(request):
    qs = MemberPayment.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(member_name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(method=status_filter)
    return render(request, 'memberpayment_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def memberpayment_create(request):
    if request.method == 'POST':
        obj = MemberPayment()
        obj.member_name = request.POST.get('member_name', '')
        obj.plan_name = request.POST.get('plan_name', '')
        obj.amount = request.POST.get('amount') or 0
        obj.payment_date = request.POST.get('payment_date') or None
        obj.method = request.POST.get('method', '')
        obj.status = request.POST.get('status', '')
        obj.next_due = request.POST.get('next_due') or None
        obj.save()
        return redirect('/memberpayments/')
    return render(request, 'memberpayment_form.html', {'editing': False})


@login_required
def memberpayment_edit(request, pk):
    obj = get_object_or_404(MemberPayment, pk=pk)
    if request.method == 'POST':
        obj.member_name = request.POST.get('member_name', '')
        obj.plan_name = request.POST.get('plan_name', '')
        obj.amount = request.POST.get('amount') or 0
        obj.payment_date = request.POST.get('payment_date') or None
        obj.method = request.POST.get('method', '')
        obj.status = request.POST.get('status', '')
        obj.next_due = request.POST.get('next_due') or None
        obj.save()
        return redirect('/memberpayments/')
    return render(request, 'memberpayment_form.html', {'record': obj, 'editing': True})


@login_required
def memberpayment_delete(request, pk):
    obj = get_object_or_404(MemberPayment, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/memberpayments/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['memberprofile_count'] = MemberProfile.objects.count()
    data['membershipplan_count'] = MembershipPlan.objects.count()
    data['memberpayment_count'] = MemberPayment.objects.count()
    return JsonResponse(data)
