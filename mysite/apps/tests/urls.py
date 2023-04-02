from django.urls import path
from . import views


urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('departments/', views.DepartmentsView.as_view(), name='departments'),
    path('department/<int:id_department>/', views.DepartmentView.as_view(), name='department'),
    path('department/<int:id_department>/sostav_kaf/', views.Sostav_kafView.as_view(), name='sostav_kaf'),
    path('department/<int:id_department>/teacher/<int:id_teacher>/subjects/', views.SubjectsView.as_view(), name='subjects'),
    path('department/<int:id_department>/teacher/<int:id_teacher>/subjects/<int:id_subject>/tests/', views.TestsView.as_view(), name='tests'),
	path('tests/', views.AllTestsView.as_view(), name='alltests'),
	path('subjects/', views.AllSubjectsView.as_view(), name='allsubjects'),
	path('profile/', views.ProfileView.as_view(), name='profile'),
	path('tests/test_add/', views.TestAddView.as_view(), name='test_add'),
	path('test/<int:id_test>/', views.TestUpdateView.as_view(), name='test_update'),
	path('tests/<int:id_test>/question_add/<int:id_question>/', views.QuestionAddView.as_view(), name='question_add'),	
	path('tests/<int:id_test>/questions_add/', views.QuestionsAddView.as_view(), name='questions_add'), #example
	path('tests/<int:id_test>/questions_update/', views.QuestionsUpdateView.as_view(), name='questions_update'), #example
	path('tests/<int:id_test>/question_update/<int:id_question>/', views.QuestionUpdateView.as_view(), name='question_update'),
	path('tests/<int:id_test>/<int:id_question>/answer_add/<int:id_answer>/', views.AnswerAddView.as_view(), name='answer_add'),
	path('tests/<int:id_test>/<int:id_question>/answer_update/<int:id_answer>/', views.AnswerUpdateView.as_view(), name='answer_update'),
	path('error/', views.error, name='error'),
	#решение тестов
	path('tests/<pk>/',views.test_view, name='test_view'),
	path('tests/<pk>/data/',views.test_data_view, name='test_data_view'),
	path('tests/<pk>/save/',views.save_test_view, name='save_test_view'),
]
