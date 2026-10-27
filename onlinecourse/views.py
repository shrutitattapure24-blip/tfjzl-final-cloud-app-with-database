from django.shortcuts import get_object_or_404, redirect, render

from .models import Choice, Course, Question, Submission


def home(request):
    courses = Course.objects.all()
    if courses:
        return redirect('course_details', course_id=courses[0].id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': None, 'lessons': [], 'questions': []})


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    questions = Question.objects.filter(lesson__course=course).order_by('order', 'id')
    return render(request, 'onlinecourse/course_details_bootstrap.html', {
        'course': course,
        'lessons': lessons,
        'questions': questions,
    })


def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = Question.objects.filter(lesson__course=course).order_by('order', 'id')
    score = 0
    total_questions = questions.count()
    results = []

    for question in questions:
        selected_choice_id = request.POST.get(f'question_{question.id}')
        selected_choice = None
        if selected_choice_id:
            selected_choice = get_object_or_404(Choice, id=selected_choice_id)
        is_correct = bool(selected_choice and selected_choice.is_correct)
        if is_correct:
            score += 1
        results.append({
            'question': question,
            'selected_choice': selected_choice,
            'is_correct': is_correct,
        })

    percentage = round((score / total_questions) * 100, 2) if total_questions else 0
    Submission.objects.create(
        course=course,
        score=score,
        total_questions=total_questions,
        percentage=percentage,
    )

    request.session['latest_exam_result'] = {
        'score': score,
        'total_questions': total_questions,
        'percentage': percentage,
        'results': [
            {
                'question_text': item['question'].question_text,
                'selected_choice_text': item['selected_choice'].choice_text if item['selected_choice'] else None,
                'is_correct': item['is_correct'],
            }
            for item in results
        ],
    }
    request.session.modified = True
    return redirect('show_exam_result', course_id=course.id)


def show_exam_result(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    result = request.session.get('latest_exam_result', {})
    score = result.get('score', 0)
    total_questions = result.get('total_questions', 0)
    percentage = result.get('percentage', 0)
    results = []

    for item in result.get('results', []):
        results.append({
            'question': type('QuestionResult', (), {'question_text': item['question_text']})(),
            'selected_choice': type('ChoiceResult', (), {'choice_text': item['selected_choice_text'] or 'No answer selected'})(),
            'is_correct': item['is_correct'],
        })

    return render(request, 'onlinecourse/exam_result.html', {
        'course': course,
        'score': score,
        'total_questions': total_questions,
        'percentage': percentage,
        'results': results,
    })
