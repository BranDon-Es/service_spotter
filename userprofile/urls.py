from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('change_password/', views.MyPasswordChangeView.as_view(), name='change_password'),
    path('edit_username/', views.edit_username, name='edit_username'),
    path('myaccount/delete_account/', views.delete_account, name='delete_account'),
    path('apply-for-vendor/', views.apply_for_vendor, name='apply_for_vendor'),
    path('my_store/', views.my_store, name='my_store'),
    path('my_store/add_service/', views.add_service, name='add_service'),
    path('my_store/edit_service/<int:pk>/', views.edit_service, name='edit_service'),
    path('my_store/delete_service/<int:pk>/', views.delete_service, name='delete_service'),
    path('vendors/<int:pk>/', views.vendor_detail, name='vendor_detail'),
]