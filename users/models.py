from django.db import models

from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):  #check for other fields
	email = models.EmailField(unique=True, blank=False)
	profile_photo = models.ImageField(upload_to='profile_images', blank=True)

	class Meta:
		verbose_name = 'Account'	