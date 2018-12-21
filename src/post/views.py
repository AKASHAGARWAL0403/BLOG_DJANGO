from django.contrib import messages
from django.http import HttpResponse , HttpResponseRedirect , Http404
from django.shortcuts import render , get_object_or_404 , redirect
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator
from urllib.parse import quote_plus
from django.utils import timezone
from django.db.models import Q
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from comments.models import Comments

def post_detail_view(request,slug=None):
	instance = get_object_or_404(Post,slug=slug)
	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			return Http404
	share_string = quote_plus(instance.content)
	comment = instance.comment
	initial_data = {
		"content_type": instance.get_content_type,
		"object_id": int(instance.id)
	}
	form = CommentForm(request.POST or None,initial=initial_data)
	if form.is_valid():
		c_type  = form.cleaned_data.get('content_type')
		content_type = ContentType.objects.get(model=c_type)
		object_id = form.cleaned_data.get('object_id')
		content = form.cleaned_data.get('content')
		parent_qs = None
		try:
			parent = int(request.POST.get('parent_id'))
		except:
			parent = None
		if parent:
			parent_obj = Comments.objects.filter(id = parent)
			if parent_obj.exists() and parent_obj.count() == 1:
				parent_qs = parent_obj.first()

		new_comment , created = Comments.objects.get_or_create(
									user = request.user,
									content_type = content_type,
									object_id = object_id,
									content = content,
									parent = parent_qs
								)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	else:
		print(form.errors)
	context = {
		"instance"  : instance,
		"share_string" : share_string,
		"comments" : comment,
		"form" : form
	}
	return render(request,"post_detail.html",context)


def post_create_view(request,*args,**kwargs):
	if not request.user.is_staff or not request.user.is_superuser:
		return Http404
	form = PostForm(request.POST or None , request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request,"Succesfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form" : form
	}
	return render(request,"post_create.html",context)


def post_list_view(request,*args,**kwargs):
	today = timezone.now().date()
	queryset_post = Post.objects.active()
	if  request.user.is_staff or  request.user.is_superuser:
		queryset_post = Post.objects.all()
	query = request.GET.get('q')
	if query:
		queryset_post = queryset_post.filter(
							Q(title__icontains=query)|
							Q(content__icontains=query)|
							Q(user__first_name__icontains=query)|
							Q(user__last_name__icontains=query)
						).distinct()

	paginator = Paginator(queryset_post, 2)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)
	queryset = paginator.get_page(page)
	context = {
		"queryset" : queryset, 
		"title" : "LIST",
		"page_request_var" : page_request_var,
		"today" : today
	}
	return render(request,"post_list.html",context)

def post_update_view(request,slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		return Http404
	instance  = get_object_or_404(Post,slug=slug)
	form  = PostForm(request.POST or None, request.FILES or None ,instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,"Succesfully updated")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"instance" : instance,
		"form"     : form 	 
	}
	return render(request,"post_create.html",context)

def post_delete_view(request,slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		return Http404
	instance  = get_object_or_404(Post,slug=slug)
	instance.delete()
	messages.success(request,"Succesfully deleted")
	return redirect('post:list')

# Create your views here.
