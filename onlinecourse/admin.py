
from django.contrib import admin
from .models import Course, Lesson, Enrollment, Question, Choice, Submission


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "lesson")
    inlines = [ChoiceInline]


class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    inlines = [QuestionInline]


class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "date_enrolled")


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "score", "total_questions", "submitted_at")


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)
