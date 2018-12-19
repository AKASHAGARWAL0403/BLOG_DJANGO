from django.contrib import messages
from django.http import HttpResponse , HttpResponseRedirect
from django.shortcuts import render , get_object_or_404 , redirect
from .models import Post
from .forms import PostForm

def post_detail_view(request,id=None):
	instance = get_object_or_404(Post,id=id)
	context = {
		"instance"  : instance
	}
	return render(request,"post_detail.html",context)


def post_create_view(request,*args,**kwargs):
	form = PostForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,"Succesfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form" : form
	}
	return render(request,"post_create.html",context)


def post_list_view(request,*args,**kwargs):
	queryset = Post.objects.all()
	context = {
		"object_list" : queryset
	}
	return render(request,"post_list.html",context)

def post_update_view(request,id=None):
	instance  = get_object_or_404(Post,id=id)
	form  = PostForm(request.POST or None,instance=instance)
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

def post_delete_view(request,id=None):
	instance  = get_object_or_404(Post,id=id)
	instance.delete()
	messages.success(request,"Succesfully deleted")
	return redirect('post:list')

# Create your views here.
