from django.urls import include
from django.conf.urls import url

from .views import (
	comment_thread_view,
	comment_delete_view
)

app_name = "comment"

urlpatterns = [
	url(r'^(?P<id>\d+)/$',comment_thread_view,name="thread"),
	url(r'^(?P<id>\d+)/delete/$', comment_delete_view,name="delete"),
]
