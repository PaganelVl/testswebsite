from django import forms
from .models import Department, Teacher, Subject, Test, Question, Answer, Result
from django.forms import ModelForm, TextInput, NumberInput, ModelChoiceField, Textarea
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory


class TestForm(ModelForm):
    class Meta:
        model = Test
        # fields = ('department','teacher','subject', 'name', 'work_time', 'questions_count','answer_count', 'statisfactorily','good', 'perfect')
        fields = '__all__'

        widgets = {
            'department': forms.Select(attrs={'class': 'form-control', 'rows': 5,'placeholder': 'Кафедра'}),
            'teacher': forms.Select(attrs={'class': 'form-control', 'rows': 5,'placeholder': 'Преподаватель'}),
            'subject': forms.Select(attrs={'class': 'form-control', 'rows': 5,'placeholder': 'Предмет'}),
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Название теста'}),
            'work_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Время выполнения (мин)'}),
            'questions_count':forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Количество вопросов'}),
            # 'answer_count':forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Количество ответов на каждый вопрос'}),
            'low': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Удовлетворительно'}),
            'good': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Хорошо'}),
            'perfect': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Отлично'}),
            'difficulty': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Сложность'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)       
        self.fields['department'].widget = forms.HiddenInput()
        self.fields['teacher'].widget = forms.HiddenInput()
        self.fields['subject'].widget = forms.HiddenInput()

class QuestionForm(ModelForm):


    class Meta:
        model = Question
        fields = '__all__'


        widgets = {
            'test': forms.Select(attrs={'class': 'form-control', 'rows': 5,'placeholder': 'Название теста','hidden': True }),
            'text': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Текст вопроса'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Вес вопроса'}),
            'num': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Порядковый номер','hidden': True }), 
            'answer_count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'количество ответов на данный вопрос','hidden': True }), 
                        
        }

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        # self.fields['num'].widget = forms.HiddenInput()
        # self.fields['test'].widget = forms.HiddenInput()
        # self.fields['answer_count'].widget = forms.HiddenInput()
        
class QuestionSetForm(ModelForm):
    class Meta:
        model = Question
        fields = ('__all__')

QuestionFormset = modelformset_factory(Question, form = QuestionForm, extra=0)     



class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'


        widgets = {
            'question': forms.Select(attrs={'class': 'form-control', 'rows': 5,'placeholder': 'Название вопроса','hidden': True }),
            'text_answer': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Текст ответа'}),
            'is_right': forms.CheckboxInput(attrs={ 'placeholder': 'Верно/Неверно'}),
            'num': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Порядковый номер','hidden': True }),               
        }

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        # self.fields['num'].widget = forms.HiddenInput()
        # self.fields['question'].widget = forms.HiddenInput()

class AnswerSetForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('__all__')

AnswerFormset = formset_factory(AnswerForm, extra=1)     

