from django.urls import include
from django.conf.urls import url

from .views import (
	post_update_view,
	post_create_view,
	post_list_view,
	post_detail_view,
	post_delete_view
)

app_name = "post"

urlpatterns = [
	url(r'^$',post_list_view,name="list"),
	url(r'^(?P<slug>[\w-]+)/delete/$',post_delete_view,name="delete"),
	url(r'^create/$',post_create_view,name="create"),
	url(r'^(?P<slug>[\w-]+)/$',post_detail_view,name="detail"),
	url(r'^(?P<slug>[\w-]+)/update/$',post_update_view,name="update")
]
