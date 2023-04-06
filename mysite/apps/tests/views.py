from django.shortcuts import render, redirect, get_object_or_404
from .models import Department, Teacher, Subject, Test, Question, Answer, Result
from .forms import TestForm, QuestionForm, AnswerForm, QuestionSetForm, QuestionFormset
from django.views.generic import ListView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.forms.formsets import formset_factory
from django.http import JsonResponse


def error(request):
	return render(request, 'main/error.html')


class MainView(CreateView):
	template_name = 'tests/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Главная'
		return context

	def get(self, request, *args, **kwargs):
		self.object = None	
		FormsetQuestion = formset_factory(QuestionForm)
		FormsetAnswer = formset_factory(AnswerForm)
		form = FormsetQuestion(prefix='question')
		form_answer = FormsetAnswer(prefix='answer')

		return self.render_to_response(
					self.get_context_data(form=form, form_answer=form_answer))


class DepartmentsView(ListView):
	model = Department
	template_name = 'tests/departments.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Кафедры'
		context['department'] = Department.objects.order_by('id')

		return context


class DepartmentView(ListView):
	model = Department
	template_name = 'tests/department.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Кафедра'
		context['department'] = Department.objects.order_by('id')
		context['id_department'] = self.kwargs['id_department']

		return context


class Sostav_kafView(ListView):
	model = Department
	template_name = 'tests/sostav_kaf.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Состав кафедры'
		context['department'] = Department.objects.order_by('id')
		context['teacher'] = Teacher.objects.order_by('id')
		context['id_department'] = self.kwargs['id_department']

		return context


class SubjectsView(ListView):
	model = Subject
	template_name = 'tests/subjects.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Предметы'
		context['department'] = Department.objects.order_by('id')
		context['teacher'] = Teacher.objects.order_by('id')
		context['subject'] = Subject.objects.order_by('id')
		context['id_department'] = self.kwargs['id_department']
		context['id_teacher'] = self.kwargs['id_teacher']

		return context


class TestsView(ListView):
	model = Test
	template_name = 'tests/tests.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Тесты'
		context['department'] = Department.objects.order_by('id')
		context['teacher'] = Teacher.objects.order_by('id')
		context['subject'] = Subject.objects.order_by('id')
		context['test'] = Test.objects.order_by('id')

		context['id_department'] = self.kwargs['id_department']
		context['id_teacher'] = self.kwargs['id_teacher']
		context['id_subject'] = self.kwargs['id_subject']

		return context


class AllTestsView(ListView):
	model = Test
	template_name = 'tests/alltests.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Тесты'
		context['department'] = Department.objects.order_by('id')
		context['teacher'] = Teacher.objects.order_by('id')
		context['subject'] = Subject.objects.order_by('id')
		context['test'] = Test.objects.order_by('id')

		return context


def test_view(request, pk):
	test = Test.objects.get(pk=pk)
	data = {
		'title': test.name,
		'obj': test,
	}

	return render(request, 'tests/test.html', data)


def test_data_view(request, pk):
	test = Test.objects.get(pk=pk)
	questions = []
	for q in test.get_questions():
		answers = []
		for a in q.get_answers():
			answers.append(a.text_answer)
		questions.append({str(q): answers})

	return JsonResponse({
			'data': questions,
			'work_time': test.work_time,
		})


def save_test_view(request, pk):
	# print(request.POST)
	if request.is_ajax():
		questions = []
		data = request.POST
		data_ = dict(data.lists())
		print(data_)
		data_.pop('csrfmiddlewaretoken')
		for k in data_.keys():
			print('key: ', k)
			question = Question.objects.get(text=k)
			questions.append(question)
		print(questions)

		user = request.user
		test = Test.objects.get(pk=pk)
		score = 0
		multiplier = 100/test.questions_count
		results = []
		correct_answer = None

		for q in questions:
			a_selected = request.POST.get(str(q))

			if a_selected != "":
				question_answers = Answer.objects.filter(question=q)
				for a in question_answers:
					if a_selected == a.text_answer:
						if a.is_right:
							score += 1
							correct_answer = a.text_answer
					else:
						if a.is_right:
							correct_answer = a.text_answer
				results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
			else:
				results.append({str(q): 'not answered'})
		score_ = score * multiplier
		Result.objects.create(test=test, user=user, rating=score_)

		if score_ >= test.low:
			return JsonResponse({'passed': True, 'score': score_, 'results': results})
		else:
			return JsonResponse({'passed': False, 'score': score_, 'results': results})


class AllSubjectsView(ListView):
	model = Subject
	template_name = 'tests/allsubjects.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Предметы'
		context['department'] = Department.objects.order_by('id')
		context['teacher'] = Teacher.objects.order_by('id')
		context['subject'] = Subject.objects.order_by('id')
		context['test'] = Test.objects.order_by('id')

		return context


class ProfileView(LoginRequiredMixin, ListView):
	model = Teacher
	template_name = 'tests/profile.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Личный кабинет'
		context['department'] = Department.objects.order_by('id')
		context['teacher'] = Teacher.objects.order_by('id')
		context['subject'] = Subject.objects.order_by('id')
		context['test'] = Test.objects.order_by('id')

		return context


class TestAddView(LoginRequiredMixin, CreateView):
	form_class = TestForm	
	template_name = 'tests/test_add.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Создание теста'	
		context['subjects'] = Subject.objects.filter(teacher = self.get_object())
		context['test'] = Test.objects.order_by('id').last().id

		return context

	def get_object(self):		
		teacher = get_object_or_404(Teacher, user = self.request.user)

		return teacher

	def get_success_url(self):	
		return reverse_lazy('questions_add', args = [Test.objects.order_by('id').last().id])
	
	def form_valid(self, form):
		self.object = form.save(commit = False)
		# if self.object.questions_count > 1 and self.object.answer_count > 1:
		self.object = form.save()

		return redirect('questions_add', self.object.id)
		# else: 
		# 	return redirect('error')

	def get(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		
		form = TestForm(
			initial={
				'department': self.get_object().department,
				'teacher': self.get_object(),
				})

		return self.render_to_response(
					self.get_context_data(form=form))


class TestUpdateView(LoginRequiredMixin, UpdateView):
	form_class = TestForm
	model = Test
	template_name = 'tests/test_add.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Редактирование теста'		
		context['test'] = Test.objects.filter(pk = self.kwargs['id_test']).first()
		context['question'] = Question.objects.filter(test = Test.objects.filter(pk = self.kwargs['id_test']).first())
		context['subjects'] = Subject.objects.filter(name = self.get_object().subject)	
		context['answer'] = Answer.objects.order_by('id')		
		if Question.objects.filter(test = Test.objects.filter(pk = self.kwargs['id_test']).first()).exists() == False:
			context['last_question'] = 0
		elif Question.objects.filter(test = Test.objects.filter(pk = self.kwargs['id_test']).first()).exists() == True:
			context['last_question'] = Question.objects.filter(test = Test.objects.filter(pk = self.kwargs['id_test']).first()).last().num

		return context

	def get_object(self):
		id_test = self.kwargs['id_test']		
		test = get_object_or_404(Test, pk=id_test)

		return test

	def form_valid(self, form):
		self.object = form.save(commit = False)
		self.object = form.save()

		return redirect('questions_add',self.kwargs['id_test'])

	def get_success_url(self):	
		return reverse_lazy('questions_add', args = [self.kwargs['id_test']])


class QuestionsAddView(LoginRequiredMixin, CreateView):
	form_class = AnswerForm, QuestionForm
	template_name = 'tests/questions_add.html'

	def get_object(self):
		id_test = self.kwargs['id_test']
		test = Test.objects.filter(pk = self.kwargs['id_test']).first()
		question = Question.objects.all().last().id+1

		return question

	def count(self):
		return Test.objects.filter(pk = self.kwargs['id_test']).first().questions_count

	def get_formset(self, form):
		return formset_factory(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Создание вопросов'	
		context['id_test'] = self.kwargs['id_test']
		context['test'] = Test.objects.filter(pk = self.kwargs['id_test']).first()

		return context

	def form_question_valid(self, form_question, form_answer):
		num_q = 0
		y = 0
		z = 0

		for f in form_question:
			num_q+=1
			self.object = f.save(commit = False)
			self.object.test = Test.objects.filter(pk = self.kwargs['id_test']).first()
			self.object.num = num_q
			f.save()		
			count = self.object.answer_count
			num_a = 0

			for z in range(count):
				num_a += 1
				print(count)
				self.object = form_answer[y].save(commit = False)				
				self.object.question = Question.objects.all().last()
				self.object.num = num_a
				form_answer[y].save()
				y += 1

		return form_question, form_answer

	def get(self, request, *args, **kwargs):
		self.object = None	
		
		FormsetQuestion = self.get_formset(QuestionForm)
		FormsetAnswer = self.get_formset(AnswerForm)
		form = FormsetQuestion(prefix = 'question')
		formset = FormsetAnswer(prefix = 'answer')
	
		return self.render_to_response(
					self.get_context_data(form=form, formset = formset))

	def post(self, request, *args, **kwargs):
		self.object = None
		FormsetQuestion = self.get_formset(QuestionForm)
		FormsetAnswer = self.get_formset(AnswerForm)
		form = FormsetQuestion(request.POST, prefix = 'question')
		formset = FormsetAnswer(request.POST, prefix = 'answer')
			
		if self.form_question_valid(form, formset):	
			print("fff")			
			return redirect('test_update', self.kwargs['id_test'])
		else:
			return redirect('error')
		#return redirect('alltests')

	def get_success_url(self):		
		return reverse_lazy('test_update', args = [self.kwargs['id_test']])


class QuestionsUpdateView(LoginRequiredMixin,CreateView):
	model = Question
	form_class = QuestionSetForm
	#template_name_suffix = '_update_form'
	template_name = 'tests/questions_update.html'

	def get_context_data(self, **kwargs):
		context = super(QuestionsUpdateView, self).get_context_data(**kwargs)
		context['test'] = Test.objects.get(pk = self.kwargs['id_test'])
		context['formset_question'] = QuestionFormset(queryset = Question.objects.filter(test = Test.objects.get(pk = self.kwargs['id_test'])))	
		#context['formset_answer'] = AnswerFormset()
		context['question'] = Question.objects.filter(test = Test.objects.get(pk = self.kwargs['id_test']))
		#context['total'] = QuestionFormset(initial=Question.objects.filter(test = Test.objects.get(pk = self.kwargs['id_test'])),prefix = 'question').total_form_count()
		
		return context

	# def get_object(self):
	# 	return Question.objects.filter(test = Test.objects.get(pk = self.kwargs['id_test'])).first()
	# def form_question_valid(self, form_question, form_answer):
	# 	num_q = 0
		
	# 	y = 0	
	# 	z = 0
	# 	for f in form_question:
	# 		num_q+=1
	# 		self.object = f.save(commit = False)
	# 		self.object.test = Test.objects.filter(pk = self.kwargs['id_test']).first()
	# 		self.object.num = num_q
	# 		f.save()		
	# 		count = self.object.answer_count
				
	# 		num_a = 0
	# 		for z in range(count):
	# 			num_a+=1
	# 			print(count)
	# 			self.object = form_answer[y].save(commit = False)				
	# 			self.object.question = Question.objects.all().last()
	# 			self.object.num = num_a
	# 			form_answer[y].save()
	# 			y+=1
	# 	return form_question,form_answer

	def post(self, request, *args, **kwargs):
		formset_question = QuestionFormset(request.POST)
		#formset_answer = AnswerFormset(request.POST)
		#for form in formset_question:
		print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
		if formset_question.is_valid():
		#if self.form_question_valid(formset_question,formset_answer):	
			print("fff")
			return self.form_valid(formset_question)
			#return self.form_valid(formset_question)			
			#return redirect('test_update', self.kwargs['id_test'])		
		else:
			print("############################")
			print(formset_question)
			print("############################")
			return self.form_invalid(formset_question)
			 
			#return redirect('error')
			#return redirect('alltests')

	def form_valid(self, formset_question):
		formset_question.save()
		#formset_answer.save()

		return redirect('test_update', self.kwargs['id_test'])

	def form_invalid(self, formset_question):
		return self.render_to_response(self.get_context_data(formset_question=formset_question))
	# form_class = formset_factory(QuestionForm)
	# template_name = 'tests/questions_update.html'
	# # model = Question

	# def get_object(self):
	# 	id_test = self.kwargs['id_test']
	# 	test = Test.objects.filter(pk = self.kwargs['id_test']).first()
	# 	FormsetQuestion = formset_factory(QuestionForm)
	# 	form = FormsetQuestion(prefix = 'question')
	# 	question = Question.objects.filter(test = test)	
	# 	return form

	def get_success_url(self):		
		return reverse_lazy('test_update', args = [self.kwargs['id_test']])

    
class QuestionAddView(LoginRequiredMixin, CreateView):
	form_class = QuestionForm	
	template_name = 'tests/question_add.html'

	def get_object(self):
		id_test = self.kwargs['id_test']
		id_question = self.kwargs['id_question']
		test = get_object_or_404(Test, pk=id_test)
		question = get_object_or_404(Question, test = test, num = id_question)

		return question

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Создание вопроса'	
		context['test'] = Test.objects.filter(pk = self.kwargs['id_test']).first()
		context['id_question'] = self.kwargs['id_question']

		return context

	def get_success_url(self):		
		if self.kwargs['id_question'] < Test.objects.filter(pk = self.kwargs['id_test']).first().questions_count:
			return reverse_lazy('question_add',kwargs={'pk': self.kwargs['id_test'], 'id_question': self.kwargs['id_question'] + 1})
		else:
			return reverse_lazy('test_update',args = [self.kwargs['id_test']])
	
	def get(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = QuestionForm(
			initial={'num': self.kwargs['id_question'], 'test': Test.objects.filter(pk = self.kwargs['id_test']).first()}
			)

		return self.render_to_response(
					self.get_context_data(form=form))


class QuestionUpdateView(LoginRequiredMixin,UpdateView):
	model = Question	
	template_name = 'tests/question_add.html'
	form_class = QuestionForm

	def get_object(self):
		id_test = self.kwargs['id_test']
		id_question = self.kwargs['id_question']
		test = get_object_or_404(Test, pk=id_test)
		question = get_object_or_404(Question, test = test, num = id_question)

		return question

	def get_success_url(self):			
		return reverse('test_update',args = [self.kwargs['id_test']])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)		
		context['update_flag'] = True
		context['title'] = 'Редактирование вопроса'			
		context['id_question'] = self.kwargs['id_question']
		context['test'] = Test.objects.filter(pk = self.kwargs['id_test']).first()
		context['question'] = Question.objects.filter(test = Test.objects.filter(pk = self.kwargs['id_test']).first(), num = self.kwargs['id_question']).first()
		if Answer.objects.filter(question = Question.objects.filter(test = Test.objects.filter(pk = self.kwargs['id_test']).first(), num = self.kwargs['id_question']).first()).exists() == False:
			context['last_answer'] = 0
		elif Answer.objects.filter(question = Question.objects.filter(test = Test.objects.filter(pk = self.kwargs['id_test']).first(), num = self.kwargs['id_question']).first()).exists() == True:
			context['last_answer'] = Answer.objects.filter(question = Question.objects.filter(test = Test.objects.filter(pk = self.kwargs['id_test']).first(), num = self.kwargs['id_question']).first()).last().num
		context['answer'] = Answer.objects.filter(question = Question.objects.filter(test = Test.objects.filter(pk = self.kwargs['id_test']).first(), num = self.kwargs['id_question']).first())

		return context


class AnswerAddView(LoginRequiredMixin,CreateView):
	form_class = AnswerForm	
	template_name = 'tests/answer_add.html'

	def get_object(self):
		id_test = self.kwargs['id_test']
		id_question = self.kwargs['id_question']
		id_answer = self.kwargs['id_answer']
		test = get_object_or_404(Test, pk=id_test)
		question = get_object_or_404(Question, test = test, num = id_question)
		answer = get_object_or_404(Answer, question = question, num = id_answer)

		return answer

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Создание ответа'	
		context['test'] = Test.objects.filter(pk = self.kwargs['id_test']).first()
		context['question'] = Question.objects.filter(test = Test.objects.filter(pk = self.kwargs['id_test']).first(), num = self.kwargs['id_question']).first()
		context['id_question'] = self.kwargs['id_question']
		context['id_answer'] = self.kwargs['id_answer']

		return context

	def get_success_url(self):	
		return reverse_lazy('question_update',args = [self.kwargs['id_test'], self.kwargs['id_question']])
	
	def get(self, request, *args, **kwargs):
		self.object = None
		form_class = self.get_form_class()
		form = AnswerForm(
			initial={
				'num': self.kwargs['id_answer'],
				'question': Question.objects.filter(test = Test.objects.filter(pk = self.kwargs['id_test']).first(), num = self.kwargs['id_question']).first()
				})

		return self.render_to_response(
					self.get_context_data(form=form))


class AnswerUpdateView(LoginRequiredMixin,UpdateView):
	model = Answer	
	template_name = 'tests/answer_add.html'
	form_class = AnswerForm

	def get_object(self):
		id_test = self.kwargs['id_test']
		id_question = self.kwargs['id_question']
		id_answer = self.kwargs['id_answer']
		test = get_object_or_404(Test, pk=id_test)
		question = get_object_or_404(Question, test = test, num = id_question)
		answer = get_object_or_404(Answer, question = question, num = id_answer)

		return answer

	def get_success_url(self):	
		return reverse_lazy('question_update',args = [self.kwargs['id_test'], self.kwargs['id_question']])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)		
		context['title'] = 'Редактирование ответа'			
		context['id_question'] = self.kwargs['id_question']
		context['test'] = Test.objects.filter(pk = self.kwargs['id_test']).first()
		context['question'] = Question.objects.filter(test = Test.objects.filter(pk = self.kwargs['id_test']).first(), num = self.kwargs['id_question']).first()
		context['id_answer'] = self.kwargs['id_answer']

		return context
