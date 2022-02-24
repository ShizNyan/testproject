from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.template import loader

from .models import Question, Answer


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:10] #последние 10 вопросов
    template = loader.get_template('questions/index.html')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'questions/index.html', context)

def tag_list(request):
    question_list_tags = Question.objects.order_by('-tags')[:5]
    template = loader.get_template('questions/index.html')
    context = {'question_list_tags': question_list_tags}
    return render(request, 'questions/index.html', context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        answers = []
        for answer in Answer.objects.all():
            if answer.question_id == question_id:
                answers.append(answer)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    except Answer.DoesNotExist:
        return render(request, 'questions/detail.html', {'question': question })
    return render(request, 'questions/detail.html', {'question': question, 'answers': answers})

def answers(request, question_id):
    return HttpResponse("These are answers to question %s." % question_id)

def create(request):
    if request.method == "POST":
        question = Question()
        question.author = request.POST.get("author")
        question.question_text = request.POST.get("question_text")
        question.pub_date = request.POST.get("pub_date")
        question.tags = request.POST.get("tags")
        question.save()
    return HttpResponse("Question has been created.")#HttpResponseRedirect("/")

def create_answer(request, question_id):
    if request.method == "POST":
        answer = Answer()
        answer.author = request.POST.get("author")
        answer.answer_text = request.POST.get("answer_text")
        answer.pub_date = request.POST.get("pub_date")
        answer.question_id = question_id
        answer.save()
    return HttpResponse("Answer has been created.")#HttpResponseRedirect("/")

def edit(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        if request.method == "POST": # and request.POST.get("author") == question.author:
            question.question_text = request.POST.get("question_text")
            question.save()
            return HttpResponse("Question has been edited.")
        else:
            return render(request, "questions/edit.html", {"question": question})
    except Question.DoesNotExist:
        return HttpResponseNotFound("<h2>Question not found</h2>")

def delete(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        question.delete()
        return HttpResponse("Question has been deleted.")
    except Question.DoesNotExist:
        return HttpResponseNotFound("<h2>Question not found</h2>")

def edit_answer(request, question_id): #работает с оговорками
    try:
        answer = Answer.objects.get(id=question_id)
        if request.method == "POST": # and request.POST.get("author") == question.author:
            answer.answer_text = request.POST.get("answer_text")
            answer.save()
            return HttpResponse("Answer has been edited.")
        else:
            return render(request, "questions/edit_answer.html", {"answer": answer})
    except Answer.DoesNotExist:
        return HttpResponseNotFound("<h2>Answer not found</h2>")

def delete_answer(request, question_id): #работает с оговорками
    try:
        answer = Answer.objects.get(id=question_id)
        answer.delete()
        return HttpResponse("Answer has been deleted.")
    except Answer.DoesNotExist:
        return HttpResponseNotFound("<h2>Answer not found</h2>")

def rating(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        if request.method == "POST": # and request.POST.get("author") == question.author:
            if request.POST.get("rating+"):
                question.rating += 1
            else:
                question.rating -= 1
            question.save()
            return HttpResponse("Rating has been edited.")
        else:
            return render(request, "questions/detail.html", {"question": question, 'answer': answer})
    except Question.DoesNotExist:
        return HttpResponseNotFound("<h2>Question not found</h2>")

def rating_answer(request, question_id):
    try:
        answer = Answer.objects.get(id=question_id)
        if request.method == "POST": # and request.POST.get("author") == question.author:
            if request.POST.get("rating+"):
                answer.rating += 1
            else:
                answer.rating -= 1
            answer.save()
            return HttpResponse("Rating has been edited.")
        else:
            return render(request, "questions/detail.html", {"question": question, 'answer': answer})
    except Answer.DoesNotExist:
        return HttpResponseNotFound("<h2>Answer not found</h2>")

def solution(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        if request.method == "POST": # and request.POST.get("author") == question.author:
            if request.POST.get("solution"):
                if question.solution:
                    question.solution = False
                else:
                    question.solution = True
            question.save()
            return HttpResponse("Question has been edited.")
        else:
            return render(request, "questions/edit.html", {"question": question})
    except Question.DoesNotExist:
        return HttpResponseNotFound("<h2>Question not found</h2>")

def solution_answer(request, question_id): #работает с оговорками
    try:
        answer = Answer.objects.get(id=question_id)
        if request.method == "POST": # and request.POST.get("author") == question.author:
            if request.POST.get("solution"):
                if answer.solution:
                    answer.solution = False
                else:
                    answer.solution = True
            answer.save()
            return HttpResponse("Answer has been edited.")
        else:
            return render(request, "questions/edit.html", {"question": question})
    except Answer.DoesNotExist:
        return HttpResponseNotFound("<h2>Answer not found</h2>")

def search(request):
    try:
        question_list = Question.objects.order_by('-pub_date')
        tags_question_list = []
        if request.method == "POST":
            for q in question_list:
                if request.POST.get("tags") in q.tags:
                    tags_question_list.append(q)
                    template = loader.get_template('questions/index.html')
                    context = {'tags_question_list': tags_question_list}
            return render(request, 'questions/index.html', context)
        else:
            return HttpResponseNotFound("<h2>Tags not found</h2>")
    except Question.DoesNotExist:
        return HttpResponseNotFound("<h2>Question not found</h2>")
