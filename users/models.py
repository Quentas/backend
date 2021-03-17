from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from datetime import datetime    


class Account(AbstractUser):  
	email = models.EmailField(unique=True, blank=False)
	profile_photo = models.ImageField(upload_to='profile_images', default='profile_images/default.jpg')

	class Meta:
		verbose_name = 'Account'	
	
	def save(self, *args, **kwargs):
		# Resizing profile image
		super().save(*args, **kwargs)
		img = Image.open(self.profile_photo.path)
		if img.height > 200 or img.width > 200:	
			output_size = (200, 200)
			img.thumbnail(output_size)
			img.save(self.profile_photo.path)
	


class Post(models.Model):
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	content = models.TextField('content', max_length=400)
	date = models.DateTimeField(auto_now=True)
	last_edited = models.DateTimeField(auto_now_add=True)

	
	def recently_published():
		return self.date >= (timezone.now() - datetime.timedelta(days = 1))

	def __str__(self):
		return self.content

	def save(self, *args, **kwargs):
		self.last_edited = datetime.now()
		super().save(*args, **kwargs)


class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	content = models.TextField('content', max_length=200)
	date = models.DateTimeField(auto_now=True)
	last_edited = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.content

	def save(self, *args, **kwargs):
		self.last_edited = datetime.now()
		super().save(*args, **kwargs)
