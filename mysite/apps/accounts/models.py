from django.db import models


class User(models.Model):
	first_name = models.CharField(max_length=100, verbose_name="Имя")
	last_name = models.CharField(max_length=100, verbose_name="Фамилия")
	username = models.CharField(max_length=100, verbose_name="Имя пользователя")
	password = models.CharField(max_length=100, verbose_name="Пароль")
	
	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'

	def __str__(self):
		return self.username
