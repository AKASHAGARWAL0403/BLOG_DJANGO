from __future__ import unicode_literals
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
class CommentManager(models.Manager):
	def all(self):
		return super(CommentManager,self).filter(parent=None)

	def filter_for_comment(self,instance,*args,**kwargs):
		content_type = ContentType.objects.get_for_model(instance.__class__)
		object_id = int(instance.id)
		return super(CommentManager,self).filter(content_type=content_type,object_id=object_id).filter(parent=None)
		#comment = Comments.objects.filter(content_type=content_type,object_id=object_id)


class Comments(models.Model):
	user        = models.ForeignKey(settings.AUTH_USER_MODEL, default=1 , on_delete=models.CASCADE)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE)
	content     = models.TextField()
	timestamp   = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.user.username)

	objects = CommentManager()

	class Meta:
		ordering = ["-timestamp"]

	def children(self):
		return Comments.objects.filter(parent=self)

	@property
	def is_parent(self):
		if self.parent is not None:
			return False
		return True