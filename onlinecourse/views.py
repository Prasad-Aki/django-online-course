
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Course, Lesson, Question, Choice, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        {"course": course}
    )


def exam(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.prefetch_related("choices").all()
    return render(
        request,
        "onlinecourse/exam.html",
        {"lesson": lesson, "questions": questions}
    )



@login_required
@require_POST
def submit(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.prefetch_related("choices")
    answers = {}
    score = 0
    total = questions.count()

    for question in questions:
        selected = request.POST.get(str(question.id))
        answers[str(question.id)] = selected

        correct_choice = question.choices.filter(is_correct=True).first()
        if correct_choice and selected == str(correct_choice.id):
            score += 1

    submission = Submission.objects.create(
        user=request.user,
        lesson=lesson,
        answers=answers,
        score=score,
        total_questions=total
    )

    return redirect("show_exam_result", submission_id=submission.id)


@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(
        Submission.objects.select_related("lesson", "user"),
        id=submission_id,
        user=request.user
    )

    results = []
    for question in submission.lesson.questions.prefetch_related("choices"):
        selected_id = submission.answers.get(str(question.id))
        selected_choice = question.choices.filter(id=selected_id).first()
        correct_choice = question.choices.filter(is_correct=True).first()

        results.append({
            "question": question,
            "selected_choice": selected_choice,
            "correct_choice": correct_choice,
            "is_correct": (
                selected_choice is not None
                and correct_choice is not None
                and selected_choice.id == correct_choice.id
            )
        })

    return render(
        request,
        "onlinecourse/exam_result.html",
        {"submission": submission, "results": results}
    )
