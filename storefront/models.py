from statistics import mode
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.db.models import Avg
from django.core.files import File
from django.core.validators import MinValueValidator, MaxValueValidator

from io import BytesIO
from PIL import Image


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class District(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Districts'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Service(models.Model):
    DRAFT = 'draft'
    WAITING_APPROVAL = 'waitingapproval'
    ACTIVE = 'active'
    DELETED = 'deleted'

    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (WAITING_APPROVAL, 'Waiting approval'),
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted')
    )

    user = models.ForeignKey(User, related_name='services', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', related_name='services', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField(blank=True)
    district = models.ForeignKey('District', related_name='services', on_delete=models.CASCADE, null=True, blank=True)
    precise_location = models.CharField(max_length=50, default='this area')
    image = models.ImageField(upload_to='uploads/service_images', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/service_images/thumbnail', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE)
    phone_number = models.CharField(max_length=20, default='1234567890')
    whatsapp_number = models.CharField(max_length=20, default='1234567890')
    email = models.EmailField(default='example@example.com')

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.image:
            self.thumbnail = self.make_thumbnail(self.image)
            self.save()
            return self.thumbnail.url
        else:
            return 'https://via.placeholder.com/240x240x.jpg'

    def average_rating(self):
        # Calculate average rating of associated reviews
        return self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']


class Review(models.Model):
    service = models.ForeignKey('Service', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField()

    class Meta:
        unique_together = ('service', 'user')  # Ensure one review per user per service

    def __str__(self):
        return f'Review by {self.user.username} for {self.service.title}'
