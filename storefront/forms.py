from django import forms
from .models import Service, Review


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('category', 'title', 'description','district', 'precise_location', 'image', 'thumbnail', 'phone_number', 'whatsapp_number', 'email')
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),

            'title': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),

            'district': forms.Select(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),

            'precise_location': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),

            'description': forms.Textarea(attrs={
            'class': 'w-full p-4 border border-gray-200'
            }),

            'image': forms.FileInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'whatsapp_number': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
            'email': forms.TextInput(attrs={
                'class': 'w-full p-4 border border-gray-200'
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], widget=forms.RadioSelect)

class VendorApplicationForm(forms.Form):
    # Add any fields you need for the vendor application form
    pass

class VendorConfirmationForm(forms.Form):
    CHOICES = [('yes', 'Yes'), ('no', 'No')]
    confirmation = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


