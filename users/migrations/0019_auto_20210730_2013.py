# Generated by Django 3.1.3 on 2021-07-30 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='last_edited',
            field=models.DateTimeField(editable=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='last_edited',
            field=models.DateTimeField(editable=False),
        ),
    ]
