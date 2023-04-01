from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import reverse
import random



class Department (models.Model):
	name = models.CharField(max_length = 100, verbose_name = "Название кафедры")
	
	class Meta:
		verbose_name ='Кафедра'
		verbose_name_plural = 'Кафедры'

	def __str__(self):
		return self.name

class Teacher(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, verbose_name = 'Никнейм пользователя')
	name = models.CharField(max_length=30, verbose_name = 'Имя')
	surname = models.CharField(max_length=30, verbose_name = 'Фамилия')
	third_name = models.CharField(max_length = 30,verbose_name = 'Отчество (если таковое имеется)', blank=True)	
	department = models.ForeignKey(Department, on_delete = models.CASCADE, verbose_name = 'Кафедра')
		

	class Meta:
		verbose_name = 'Преподаватель'
		verbose_name_plural = 'Преподаватели'


	def __str__(self):
		return ' %s %s %s' %(self.surname, self.name, self.third_name)

class Subject(models.Model):
	name = models.CharField(max_length = 50, verbose_name = 'Название предмета')
	department = models.ForeignKey(Department, on_delete = models.CASCADE, verbose_name = 'Кафедра', null = True)
	teacher = models.ForeignKey(Teacher, on_delete = models.CASCADE, verbose_name = 'Преподаватель', null = True)

	class Meta:
		verbose_name = 'Предмет'
		verbose_name_plural = 'Предметы'


	def __str__(self):
		return self.name

DIFF_CHOICES = (
		('Легко','Легко'),
		('Средне','Средне'),
		('Тяжело','Тяжело'),

	)

class Test(models.Model):
	department = models.ForeignKey(Department, on_delete = models.CASCADE, null = True, verbose_name = 'Кафедра')
	teacher = models.ForeignKey(Teacher, on_delete = models.CASCADE, verbose_name = 'Преподаватель', null = True)    
	subject = models.ForeignKey(Subject, on_delete = models.CASCADE,null = True, verbose_name = 'Предмет')
	name = models.CharField(max_length=50, verbose_name='Название теста')
	work_time = models.IntegerField(default=1,verbose_name='Время выполнения (мин)')
	questions_count = models.IntegerField(default=1,verbose_name='Количество вопросов')
	# answer_count = models.IntegerField(default=1,verbose_name = 'Количество ответов на каждый вопрос')
	low = models.IntegerField(default=1,verbose_name='Удовлетворительно')
	good = models.IntegerField(default=1,verbose_name='Хорошо')
	perfect = models.IntegerField(default=1,verbose_name='Отлично')
	difficulty = models.CharField(max_length=6,choices=DIFF_CHOICES, default='',verbose_name='Сложность')

	class Meta:
		ordering = ('name',)
		verbose_name = 'Тест'
		verbose_name_plural = 'Тесты'

	def __str__(self):
		return f"{self.name}-{self.subject}-{self.teacher}"

	def get_questions(self):
		questions = list(self.question_set.all())
		random.shuffle(questions)
		return questions[:self.questions_count]

	def get_absolute_url(self):
		return reverse('alltests')


	def length(n):
		i = 0
		
		mas1 = [0]*n.questions_count
		
		while i < n.questions_count:
		    mas1[i] = i
		    i += 1
		
		return mas1

class Question(models.Model):
	test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест',null = True)
	text = models.TextField(verbose_name='Текст вопроса', null = True)
	# whileight = models.FloatField(default=1, verbose_name='Вес', null = True)
	num = models.IntegerField(default=1,verbose_name='Порядковый номер', null = True)
	answer_count = models.IntegerField(default=1,verbose_name='количсество ответов на данный вопрос', null = True)
	def __str__(self):
		return str(self.text)

	def get_absolute_url(self):
		return reverse('test_update',args = [self.kwargs['id_test']])

	def get_answers(self):
		return self.answer_set.all()

	class Meta:
		verbose_name = 'Вопрос'
		verbose_name_plural = 'Вопросы'




class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос', null = True,default = Question.objects.filter().first())
    text_answer = models.CharField(max_length=100, verbose_name='Текст ответа')
    is_right = models.BooleanField(verbose_name='Верно/Неверно')
    num = models.IntegerField(default=1,verbose_name='Порядковый номер')
    
    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text_answer}, is_right: {self.is_right}"

class Result(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест')
    user = models.ForeignKey(User,on_delete=models.CASCADE, null = True)
    datetime = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Время завершения")
    rating =models.FloatField(verbose_name="Проценты")

    def __str__(self):
    	return str(self.pk)

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'

class QuestionsInline(admin.TabularInline):
    model = Answer

