from django.contrib import admin

from .models import Subject,Teacher, Department, Test, Question, Answer, Result



class DepartmentAdmin(admin.ModelAdmin):
	list_display = ('id','name')
	list_display_links = ('id','name')
	search_field = ('name')


class TeacherAdmin(admin.ModelAdmin):
	list_display = ('id','user','__str__', 'department')
	list_display_links = ('id','user', '__str__', 'department')
	search_field = ('name')

class SubjectAdmin(admin.ModelAdmin):
	list_display = ('id', 'name','teacher', 'department')
	list_display_links = ('id','name','teacher', 'department')
	search_field = ('name')

class QuestionInline(admin.TabularInline):
	model = Question

class TestAdmin(admin.ModelAdmin):
	inlines = [QuestionInline]
	list_display = ('id','name','subject','teacher','department')
	list_display_links = ('id','name','subject','teacher','department')
	search_field = ('name')


class AnswerInline(admin.TabularInline):
	model = Answer


class QuestionAdmin(admin.ModelAdmin):
	inlines = [AnswerInline]
	list_display = ('id','num','test','text')
	list_display_links = ('id','num','test','text')
	search_field = ('text')

class AnswerAdmin(admin.ModelAdmin):
	list_display = ('id','num','text_answer','question','is_right')
	list_display_links = ('id','num','text_answer','question','is_right')
	search_field = ('id')




admin.site.register(Department, DepartmentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)

admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Result)

