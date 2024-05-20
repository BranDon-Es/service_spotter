from django.contrib import messages
from django.contrib.auth import login,logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify

from .models import Userprofile

from storefront.forms import ServiceForm, VendorApplicationForm, VendorConfirmationForm
from storefront.models import Service, Category


def apply_for_vendor(request):
    if request.method == 'POST':
        form = VendorConfirmationForm(request.POST)
        if form.is_valid():
            confirmation = form.cleaned_data.get('confirmation')
            if confirmation == 'yes':
                request.user.userprofile.is_vendor = True
                request.user.userprofile.save()
                return redirect('myaccount')  # Redirect to "My Account" page with success message
            else:
                return redirect('myaccount')  # Redirect to "My Account" page with different message
    else:
        form = VendorConfirmationForm()
    return render(request, 'userprofile/vendor_confirmation.html', {'form': form})


def confirm_vendor_application(request):
    if request.method == 'POST':
        form = VendorConfirmationForm(request.POST)
        if form.is_valid():
            confirmation = form.cleaned_data.get('confirmation')
            if confirmation == 'yes':
                request.user.userprofile.is_vendor = True
                request.user.userprofile.save()
                return redirect('myaccount')  # Redirect to "My Account" page with success message
            else:
                return redirect('myaccount')  # Redirect to "My Account" page with different message
    else:
        form = VendorConfirmationForm()
    return render(request, 'vendor_confirmation.html', {'form': form})

def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)
    services = user.services.filter(status=Service.ACTIVE)

    return render(request, 'userprofile/vendor_detail.html', {
        'user': user,
        'services': services
    })


@login_required
def my_store(request):
    services = request.user.services.exclude(status=Service.DELETED)

    return render(request, 'userprofile/my_store.html', {
        'services': services
    })


@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)

        if form.is_valid():
            title = request.POST.get('title')

            service = form.save(commit=False)
            service.user = request.user
            service.slug = slugify(title)
            service.save()

            messages.success(request, 'The service was added.')

            return redirect('my_store')

    else:
        form = ServiceForm()

    return render(request, 'userprofile/service_form.html', {
        'title': 'Add service',
        'form': form
    })


@login_required
def edit_service(request, pk):
    service = Service.objects.filter(user=request.user).get(pk=pk)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)

        if form.is_valid():
            form.save()

            messages.success(request, 'The changes have been made.')

            return redirect('my_store')
    else:
        form = ServiceForm(instance=service)

    return render(request, 'userprofile/service_form.html', {
        'title': 'Edit service',
        'service': service,
        'form': form
    })


def delete_service(request, pk):
    service = Service.objects.filter(user=request.user).get(pk=pk)
    service.status = Service.DELETED
    service.save()

    messages.success(request, 'The service was deleted.')

    return redirect('my_store')

@login_required
def myaccount(request):
    return render(request, 'userprofile/myaccount.html')


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            userprofile = Userprofile.objects.create(user=user)
            return redirect('frontpage')

    else:
        form = UserCreationForm()

    # Pass the form.errors dictionary to the template
    return render(request, 'userprofile/signup.html', {
        'form': form,
        'errors': form.errors  # This will include any validation errors in the form
    })


class MyPasswordChangeView(PasswordChangeView):
    template_name = 'myaccount.html'  # Use your template name here
    success_url = reverse_lazy('myaccount')  # Redirect to myaccount on success

    def form_valid(self, form):
        messages.success(self.request, 'Your password was successfully updated.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to update password. Please correct the errors.')
        return super().form_invalid(form)
def edit_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        user = request.user
        if new_username and new_username != user.username:
            user.username = new_username
            user.save()
            messages.success(request, 'Your username was successfully updated.')
            return redirect('myaccount')
        else:
            messages.error(request, 'Failed to update username. Please try again.')
    return redirect('myaccount')  # Redirect to my_account page regardless

@login_required
def delete_account(request):
    if request.method == 'POST':
        if 'delete_account' in request.POST:
            request.user.delete()
            logout(request)
            return redirect('frontpage')
        elif 'cancel' in request.POST:
            return redirect('frontpage')     
        
    return render(request, 'userprofile/delete_account.html')
    
