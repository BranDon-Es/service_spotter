from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.search, name = 'search'),
    path('make_appointment/<int:service_id>/', views.make_appointment, name='make_appointment'),
    path('<slug:slug>/', views.category_detail, name='category_detail'),
    path('<slug:category_slug>/<slug:slug>/', views.service_detail, name='service_detail'),
]