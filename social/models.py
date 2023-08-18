from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User 
# Create your models here.

class Post(models.Model):
	image = models.ImageField(default='default.jpg', upload_to = 'post_pics')
	caption = models.TextField(default='')
	date_posted = models.DateTimeField(default=timezone.now)
	total_like = models.IntegerField(default=0)
	author = models.ForeignKey(User, on_delete = models.CASCADE) 


	def __str__(self):
		return self.author.username

	
class Profile(models.Model):
	#author = models.ForeignKey(User, on_delete = models.CASCADE) 
	author = models.OneToOneField(User, related_name ='profile', on_delete=models.CASCADE)

	bio = models.TextField(default='')
	image = models.ImageField(default='default.jpg', upload_to = 'profile_pics')
	

	def __str__(self):
		return self.author.username + 'profile'

class FollowersCount(models.Model):
	follower = models.CharField(max_length=100)
	user = models.CharField(max_length=100)

	def __str__(self):
		return self.user


 