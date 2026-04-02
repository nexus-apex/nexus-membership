from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('memberprofiles/', views.memberprofile_list, name='memberprofile_list'),
    path('memberprofiles/create/', views.memberprofile_create, name='memberprofile_create'),
    path('memberprofiles/<int:pk>/edit/', views.memberprofile_edit, name='memberprofile_edit'),
    path('memberprofiles/<int:pk>/delete/', views.memberprofile_delete, name='memberprofile_delete'),
    path('membershipplans/', views.membershipplan_list, name='membershipplan_list'),
    path('membershipplans/create/', views.membershipplan_create, name='membershipplan_create'),
    path('membershipplans/<int:pk>/edit/', views.membershipplan_edit, name='membershipplan_edit'),
    path('membershipplans/<int:pk>/delete/', views.membershipplan_delete, name='membershipplan_delete'),
    path('memberpayments/', views.memberpayment_list, name='memberpayment_list'),
    path('memberpayments/create/', views.memberpayment_create, name='memberpayment_create'),
    path('memberpayments/<int:pk>/edit/', views.memberpayment_edit, name='memberpayment_edit'),
    path('memberpayments/<int:pk>/delete/', views.memberpayment_delete, name='memberpayment_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
