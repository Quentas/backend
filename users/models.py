from django.db import models

from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):  
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


class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	content = models.TextField('content', max_length=200)
	date = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.content