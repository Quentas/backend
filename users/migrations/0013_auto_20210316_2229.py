# Generated by Django 3.1.3 on 2021-03-16 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20210316_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_photo',
            field=models.ImageField(default='profile_images/default.jpg', upload_to='profile_images'),
        ),
    ]