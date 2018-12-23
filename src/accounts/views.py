from django.shortcuts import render , redirect

# Create your views here.
from django.contrib.auth import (
		login,
		logout,
		authenticate
	)

from .forms import ( LoginForm , UserRegisterForm )

def login_view(request):
	print(request.user.is_authenticated)
	nex = request.GET.get('next')
	print(nex)
	form  = LoginForm(request.POST or None)
	context = {
		"form" : form,
		"title" : "Login"
	}
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user  = authenticate(username=username,password=password)
		login(request,user)
		print(request.user.is_authenticated)
		if nex:
			return  redirect(nex)
		return redirect('/')

	return render(request,"form.html",context)

def logout_view(request):
	logout(request)
	return redirect('/')

def register_view(request):
	form = UserRegisterForm(request.POST or None)
	context = {
		"form" : form,
		"title" : "Register"
	}
	nex = request.GET.get('next')
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		n_user  = authenticate(username=user.username,password=password)
		login(request,n_user)
		if nex:
			return  redirect(nex)
		return redirect('/')
	return render(request,"form.html",context)
