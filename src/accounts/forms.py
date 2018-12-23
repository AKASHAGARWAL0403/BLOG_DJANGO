from django.contrib.auth import (
		login,
		logout,
		authenticate,
		get_user_model
	)
from django import forms

User =  get_user_model()

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self,*agrs,**kwargs):
		username  = self.cleaned_data.get("username")
		password  = self.cleaned_data.get("password")
		user = authenticate(username=username,password=password)
		if not user:
			raise forms.ValidationError("this user does not exits")
		if not user.check_password(password):
			raise forms.ValidationError("This is not the correct password")
		return super(LoginForm,self).clean()

class UserRegisterForm(forms.ModelForm):
	email2 = forms.EmailField(label='Confirm Email')
	email = forms.EmailField(label='Email'),
	password = forms.CharField(widget=forms.PasswordInput)
	first_name = forms.CharField()
	last_name = forms.CharField()
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'email2',
			'password',
			'first_name',
			'last_name'
		]
	def clean_email2(self):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email2 != email:
			raise forms.ValidationError("Emails must match")
		e_qs = User.objects.filter(email=email)
		if e_qs.exists():
			raise forms.ValidationError("Error is used previously")
		return email