from django.db.models import Avg, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.conf import settings
import requests
from .models import Category, Service, Review
from .forms import ReviewForm


def make_appointment(request, service_id):
    service = Service.objects.get(pk=service_id)
    context = {
        'service': service,
        'service_title': service.title  # Assuming the title field name is 'title'
    }
    return render(request, 'make_appointment.html', context)


def search(request):
    query = request.GET.get('query', '')
    services = Service.objects.filter(status=Service.ACTIVE).filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )

    for service in services:
        service.avg_rating = service.average_rating()

    context = {
        'services': services
    }

    return render(request, 'search.html', {
        'query': query,
        'services': services
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    services = category.services.filter(status=Service.ACTIVE)

    return render(request, 'category_detail.html', {
        'category': category,
        'services': services,
    })


def service_detail(request, category_slug, slug):
    service = get_object_or_404(Service, slug=slug, status=Service.ACTIVE)
    reviews = Review.objects.filter(service=service)
    avg_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']

    user_review = None
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.service = service
            review.user = request.user
            review.save()
            return redirect('service_detail', category_slug=category_slug, slug=slug)
    else:
        form = ReviewForm()

    # Check if the user has already reviewed this service
    if request.user.is_authenticated:
        user_review = Review.objects.filter(service=service, user=request.user).first()

    return render(request, 'service_detail.html', {
        'service': service,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'form': form,
        'user_review': user_review
    })



