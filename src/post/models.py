from __future__ import unicode_literals
from django.db import models
from django.urls import reverse

class Post(models.Model):
	title = models.CharField(max_length= 150)
	content = models.TextField()
	updated = models.DateTimeField(auto_now = True,auto_now_add = False)
	timestamp = models.DateTimeField(auto_now = False , auto_now_add = True)

	def get_absolute_url(self):
		return reverse('post:detail',kwargs={"id":self.id})
# Create your models here.
