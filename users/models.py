from django.db import models

from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):  #check for other fields
	email = models.EmailField(unique=True, blank=False)
	profile_photo = models.ImageField(upload_to='profile_images', blank=True)

	class Meta:
		verbose_name = 'Account'	

class Post(models.Model):
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	content = models.TextField('content', max_length=400)
	date = models.DateTimeField(auto_now=True)
	
	def recently_published():
		return self.date >= (timezone.now() - datetime.timedelta(days = 1))

	def __str__(self):
		return self.content