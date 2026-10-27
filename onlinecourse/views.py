from django.shortcuts import get_object_or_404, redirect, render

from .models import Choice, Course, Enrollment, Learner, Question, Submission


def home(request):
    courses = Course.objects.all()
    if courses:
        return redirect('course_details', course_id=courses[0].id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': None, 'lessons': [], 'questions': []})


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    questions = Question.objects.filter(course=course).order_by('order', 'id')
    return render(request, 'onlinecourse/course_details_bootstrap.html', {
        'course': course,
        'lessons': lessons,
        'questions': questions,
    })


def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    learner, _ = Learner.objects.get_or_create(name='Demo Learner', email='demo@example.com')
    enrollment, _ = Enrollment.objects.get_or_create(learner=learner, course=course)
    questions = Question.objects.filter(course=course).order_by('order', 'id')

    selected_choices = []
    score = 0
    total_questions = questions.count()

    for question in questions:
        choice_id = request.POST.get(f'question_{question.id}')
        choice = get_object_or_404(Choice, id=choice_id) if choice_id else None
        if choice and choice.is_correct:
            score += question.grade
        if choice:
            selected_choices.append(choice)

    percentage = round((score / (sum(q.grade for q in questions) or 1)) * 100, 2) if questions else 0
    submission = Submission.objects.create(
        enrollment=enrollment,
        score=score,
        total_questions=total_questions,
        percentage=percentage,
    )
    submission.choices.set(selected_choices)

    request.session['latest_exam_result'] = {
        'course_id': course.id,
        'score': score,
        'total_questions': total_questions,
        'percentage': percentage,
        'submission_id': submission.id,
        'results': [
            {
                'question_text': question.question_text,
                'selected_choice_text': (
                    next((choice.choice_text for choice in selected_choices if choice.question_id == question.id), 'No answer selected')
                ),
                'is_correct': any(
                    choice.question_id == question.id and choice.is_correct for choice in selected_choices
                ),
            }
            for question in questions
        ],
    }
    request.session.modified = True
    return redirect('show_exam_result', submission_id=submission.id)


def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    result = request.session.get('latest_exam_result', {})
    course = submission.enrollment.course
    score = result.get('score', submission.score)
    total_questions = result.get('total_questions', submission.total_questions)
    percentage = result.get('percentage', submission.percentage)

    results = []
    for item in result.get('results', []):
        results.append({
            'question': {'question_text': item['question_text']},
            'selected_choice': {'choice_text': item['selected_choice_text']},
            'is_correct': item['is_correct'],
        })

    if not results and submission.choices.exists():
        for choice in submission.choices.all():
            results.append({
                'question': {'question_text': choice.question.question_text},
                'selected_choice': {'choice_text': choice.choice_text},
                'is_correct': choice.is_correct,
            })

    return render(request, 'onlinecourse/exam_result.html', {
        'course': course,
        'score': score,
        'total_questions': total_questions,
        'percentage': percentage,
        'results': results,
    })
