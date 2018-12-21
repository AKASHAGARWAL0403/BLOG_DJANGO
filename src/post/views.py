from django.contrib import messages
from django.http import HttpResponse , HttpResponseRedirect , Http404
from django.shortcuts import render , get_object_or_404 , redirect
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator
from urllib.parse import quote_plus
from django.utils import timezone
from django.db.models import Q

def post_detail_view(request,slug=None):
	instance = get_object_or_404(Post,slug=slug)
	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			return Http404
	share_string = quote_plus(instance.content)
	context = {
		"instance"  : instance,
		"share_string" : share_string
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
