# Generated by Django 3.1.3 on 2021-08-01 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_comment_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='bio',
            field=models.TextField(blank=True, max_length=200, verbose_name='bio'),
        ),
    ]
