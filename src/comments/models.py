from __future__ import unicode_literals
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
class CommentManager(models.Manager):
	def filter_for_comment(self,instance,*args,**kwargs):
		content_type = ContentType.objects.get_for_model(instance.__class__)
		object_id = int(instance.id)
		return super(CommentManager,self).filter(content_type=content_type,object_id=object_id)
		#comment = Comments.objects.filter(content_type=content_type,object_id=object_id)


class Comments(models.Model):
	user        = models.ForeignKey(settings.AUTH_USER_MODEL, default=1 , on_delete=models.CASCADE)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	content     = models.TextField()
	timestamp   = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.user.username)

	objects = CommentManager()

	class Meta:
		ordering = ["-timestamp"]