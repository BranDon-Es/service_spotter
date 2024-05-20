from django.shortcuts import render
from storefront.models import Service
def frontpage(request):
    services =Service.objects.filter(status=Service.ACTIVE)[0:6]

    # Calculate average rating for each service
    for service in services:
        service.avg_rating = service.average_rating()

    context = {
        'services': services
    }

    return render(request, 'frontpage.html', {
        'services': services
    })


def about(request):
    return render(request, 'about.html')


def custom_404(request, exception):
    return render(request, '404.html', status=404)


