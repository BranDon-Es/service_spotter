# Generated by Django 5.0.2 on 2024-03-20 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storefront', '0003_service_email_service_phone_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/service_images/thumbnail/'),
        ),
    ]
