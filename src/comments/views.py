from django.shortcuts import render,get_object_or_404
from .models import Comments
from .forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponseRedirect , Http404 , HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/login/')
def comment_delete_view(request,id):
	try:
		obj =  Comments.objects.get(id=id)
	except:
		return Http404
	context =  {
		"object" : obj
	}
	if request.user != obj.user:
		response = HttpResponse("You dont have the permission to delete this")
		response.status_code = 403
		return response

	if request.method == "POST" :
		parent_obj_url = obj.content_object.get_absolute_url()
		obj.delete()
		messages.success(request,"It was deleted successfully")
		return HttpResponseRedirect(parent_obj_url)
	return render(request,"comment_delete.html",context)

def comment_thread_view(request,id):
	try:
		obj = Comments.objects.get(id=id)
	except:
		return Http404
	intial_obj = {
		"content_type" : obj.content_type,
		"object_id" : obj.object_id
	}
	if not obj.is_parent:
		obj = obj.parent
	form = CommentForm(request.POST or None,initial=intial_obj)
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
		return HttpResponseRedirect(new_comment.parent.get_absolute_url())

	else:
		print(form.errors)

	context = {
		"object" : obj,
		"form"   : form
 	}
	return render(request,"comment_thread.html",context)