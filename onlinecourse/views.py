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

    total_score = 0
    possible_score = 0
    selected_ids = []
    results = []

    for question in questions:
        possible_score += question.grade
        selected_choice_id = request.POST.get(f'question_{question.id}')
        selected_choice = Choice.objects.filter(id=selected_choice_id).first() if selected_choice_id else None
        if selected_choice_id:
            selected_ids.append(selected_choice_id)
        score_for_question = question.is_get_score(selected_choice)
        total_score += score_for_question
        results.append({
            'question_text': question.question_text,
            'selected_choice_text': selected_choice.choice_text if selected_choice else 'No answer selected',
            'is_correct': bool(selected_choice and selected_choice.is_correct),
            'score': score_for_question,
        })

    percentage = round((total_score / possible_score) * 100, 2) if possible_score else 0
    submission = Submission.objects.create(
        enrollment=enrollment,
        score=total_score,
        total_questions=questions.count(),
        percentage=percentage,
    )

    selected_choices = []
    for question in questions:
        choice_id = request.POST.get(f'question_{question.id}')
        if choice_id:
            selected_choice = get_object_or_404(Choice, id=choice_id)
            selected_choices.append(selected_choice)
    submission.choices.set(selected_choices)

    request.session['latest_exam_result'] = {
        'course_id': course.id,
        'submission_id': submission.id,
        'total_score': total_score,
        'possible_score': possible_score,
        'selected_ids': selected_ids,
        'results': results,
    }
    request.session.modified = True
    return redirect('show_exam_result', course_id=course.id, submission_id=submission.id)


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, id=course_id)
    submission = get_object_or_404(Submission, id=submission_id, enrollment__course=course)
    result = request.session.get('latest_exam_result', {})

    selected_ids = result.get('selected_ids', [])
    total_score = 0
    possible_score = 0
    results = []

    for question in Question.objects.filter(course=course).order_by('order', 'id'):
        selected_choice = Choice.objects.filter(id__in=selected_ids, question=question).first() if selected_ids else None
        score = question.is_get_score(selected_choice)
        total_score += score
        possible_score += question.grade
        results.append({
            'question_text': question.question_text,
            'selected_choice_text': selected_choice.choice_text if selected_choice else 'No answer selected',
            'is_correct': bool(selected_choice and selected_choice.is_correct),
            'score': score,
        })

    if not selected_ids and submission.choices.exists():
        for choice in submission.choices.all():
            total_score += choice.question.is_get_score(choice)
            possible_score += choice.question.grade
            results.append({
                'question_text': choice.question.question_text,
                'selected_choice_text': choice.choice_text,
                'is_correct': choice.is_correct,
                'score': choice.question.is_get_score(choice),
            })

    return render(request, 'onlinecourse/exam_result_bootstrap.html', {
        'course': course,
        'submission': submission,
        'selected_ids': selected_ids,
        'total_score': total_score,
        'possible_score': possible_score,
        'grade': total_score,
        'possible': possible_score,
        'percentage': round((total_score / possible_score) * 100, 2) if possible_score else 0,
        'results': results,
    })
