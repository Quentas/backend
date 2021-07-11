from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from datetime import datetime
from django.db.models.deletion import CASCADE, DO_NOTHING    
from django.utils import timezone


class Account(AbstractUser):  
	username = models.CharField(max_length=15, unique=True, blank=False)
	email = models.EmailField(unique=True, blank=False)
	profile_photo = models.ImageField(upload_to='profile_images', default='profile_images/default.jpg')

	class Meta:
		verbose_name = 'Account'	
	'''
	def save(self, *args, **kwargs):
		# Resizing profile image
		super().save(*args, **kwargs)
		img = Image.open(self.profile_photo.path)
		if img.height > 200 or img.width > 200:	
			output_size = (200, 200)
			img.thumbnail(output_size)
			img.save(self.profile_photo.path)
	'''

class Picture(models.Model):
	image = models.ImageField(upload_to='pictures', blank=True) # should it be blank ???


class Post(models.Model):
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	content = models.TextField('content', max_length=400)
	date = models.DateTimeField(editable=False)
	last_edited = models.DateTimeField()
	images = models.ManyToManyField(Picture, related_name='post_images', blank=True)
	
	def recently_published(self):
		return self.date >= (timezone.now() - datetime.timedelta(days = 1))

	def __str__(self):
		return self.content

	def save(self, *args, **kwargs):
		if not self.id:
			self.date  = timezone.now()
		self.last_edited = timezone.now()
		return super(Post, self).save(*args, **kwargs)

	@property
	def count_replies(self):
		return Comment.objects.filter(post=self).count()


class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	content = models.TextField('content', max_length=200)
	date = models.DateTimeField(editable=False)
	last_edited = models.DateTimeField()
	images = models.ManyToManyField(Picture, related_name='comment_images', blank=True)
	parent = models.ForeignKey("self", null=True, blank=True, on_delete=CASCADE)
	
	def __str__(self):
		return self.content

	def save(self, *args, **kwargs):
		if not self.id:
			self.date  = timezone.now()
		self.last_edited = timezone.now()
		return super(Comment, self).save(*args, **kwargs)

	@property
	def count_replies(self):
		return Comment.objects.filter(parent=self).count()
