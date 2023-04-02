from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login


class MySiteLoginView(LoginView):
	template_name ='accounts/login.html'
	form_class = LoginForm
	success_url = reverse_lazy('main')

	def get_success_url(self):
		return self.success_url

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['title'] = 'Авторизация'
		print(context)
		return context


class MySiteLogout(LogoutView):
	next_page = reverse_lazy('main')


class RegisterUserView(CreateView):
	model = User
	template_name = 'accounts/register_page.html'
	form_class = RegisterForm
	success_url = reverse_lazy('main')
	success_msg = 'Пользователь успешно создан'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['title'] = 'Регистрация'
		print(context)
		return context

	def form_valid(self, form):
		form_valid = super().form_valid(form)
		username = form.cleaned_data["username"]
		password = form.cleaned_data["password"]
		aut_user = authenticate(username = username, password = password)
		login(self.request, aut_user)
		return form_valid
