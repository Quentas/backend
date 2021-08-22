from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser
from PIL import Image
from datetime import datetime
from django.db.models.deletion import CASCADE, DO_NOTHING    
from django.utils import timezone


class Account(AbstractUser):  
	username = models.CharField(max_length=15, unique=True, blank=False)
	email = models.EmailField(unique=True, blank=False)
	profile_photo = models.ImageField(upload_to='profile_images', default='profile_images/default.jpg')
	bio = models.TextField('bio', max_length=200, blank=True)
	first_name = models.CharField(blank=True, max_length=15, verbose_name='first name')
	last_name = models.CharField(blank=True, max_length=15, verbose_name='last name')
	subscribed_to = models.ManyToManyField("self", blank=True, related_name='subscribed_by', symmetrical=False)
	provider = models.CharField(max_length=20, blank=True, unique=False)
	id_token = models.TextField(blank=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	class Meta:
		verbose_name = 'Account'	
	
	def __str__(self):
		return self.username

	def save(self, *args, **kwargs):
		# Resizing profile image
		super().save(*args, **kwargs)
		img = Image.open(self.profile_photo.path)
		if img.height > 200 or img.width > 200:	
			output_size = (200, 200)
			img.thumbnail(output_size)
			img.save(self.profile_photo.path)

	@property
	def user_posts_count(self):
		return Post.objects.filter(user__username=self.username).count()

	@property
	def user_comments_count(self):
		return Comment.objects.filter(user__username=self.username).count()

	@property
	def user_likes_count(self):
		return self.post_like.count() + self.comment_like.count()

	@property
	def following_count(self):
		return self.subscribed_to.count()
	
	@property
	def followers_count(self):
		return Account.objects.filter(subscribed_to__username = self.username).count()


class Picture(models.Model):
	image = models.ImageField(upload_to='pictures', blank=False) 


class Post(models.Model):
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	content = models.TextField('content', max_length=400)
	pub_date = models.DateTimeField(editable=False)
	last_edited = models.DateTimeField(editable=False)
	images = models.ManyToManyField(Picture, related_name='post_images', blank=True)
	likes = models.ManyToManyField(Account, related_name='post_like', blank=True)
	bookmark = models.ManyToManyField(Account, related_name='booked_post', blank=True)

	def __str__(self):
		return self.content

	def save(self, *args, **kwargs):
		if not self.id:
			self.pub_date  = timezone.now()
		self.last_edited = timezone.now()
		return super(Post, self).save(*args, **kwargs)

	@property
	def comments_count(self):
		return Comment.objects.filter(post=self).count()

	@property
	def total_likes(self):
		return self.likes.count()


class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	content = models.TextField('content', max_length=200)
	pub_date = models.DateTimeField(editable=False)
	last_edited = models.DateTimeField(editable=False)
	images = models.ManyToManyField(Picture, related_name='comment_images', blank=True)
	parent = models.ForeignKey("self", null=True, blank=True, on_delete=CASCADE)
	likes = models.ManyToManyField(Account, related_name='comment_like', blank=True)
	bookmark = models.ManyToManyField(Account, related_name='booked_comment', blank=True)

	
	def __str__(self):
		return self.content

	def save(self, *args, **kwargs):
		if not self.id:
			self.pub_date  = timezone.now()
		self.last_edited = timezone.now()
		return super(Comment, self).save(*args, **kwargs)

	@property
	def comments_count(self):
		return Comment.objects.filter(parent=self).count()

	@property
	def total_likes(self):
		return self.likes.count()
