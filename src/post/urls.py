from django.urls import path,include

from .views import (
	post_update_view,
	post_create_view,
	post_list_view,
	post_detail_view,
	post_delete_view
)

app_name = "post"

urlpatterns = [
	path('',post_list_view,name="list"),
	path('<int:id>/delete/',post_delete_view,name="delete"),
	path('create/',post_create_view,name="create"),
	path('<int:id>/detail/',post_detail_view,name="detail"),
	path('<int:id>/update/',post_update_view,name="update")
]
