# Generated by Django 3.1.3 on 2021-03-16 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20210316_0111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_photo',
            field=models.ImageField(default='default.jpg', upload_to='profile_images'),
        ),
    ]
