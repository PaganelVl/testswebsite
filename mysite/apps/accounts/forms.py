from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm, forms.ModelForm):

	class Meta:
		model = User
		fields = ('username','password')	

		widgets = {
			
			'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Логин'}),
			'password': forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Пароль'}),			     
		}
	# widgets = {
	# 	'password': forms.PasswordInput()
	# }

	# def __init__(self,*args,**kwargs):
	# 	super().__init__(*args,**kwargs)
	# 	self.fields['username'].label ='Логин'
	# 	self.fields['password'].label ='Пароль'

	# def clean(self):
	# 	username = self.cleaned_data['username']
	# 	password = self.cleaned_data['password']
	# 	if not User.objects.filter(username=username).exists():
	# 		raise forms.ValidationError(f'Пользователь с логином {username} не найден.')
	# 	user = User.objects.filter(username=username).first()
	# 	if user:
	# 		if not user.check_password(password):
	# 			raise forms.ValidationError(f'Неверный пароль')
	# 	return self.cleaned_data


class RegisterForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('first_name','last_name','username','password')	
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Имя'}),
			'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Фамилия'}),
			'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Логин'}),
			'password': forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Пароль'}),			     
		}

	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['username'].label ='Логин'
		self.fields['password'].label ='Пароль'

	def save(self, commit = True):
		user = super().save(commit = False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user