from django.shortcuts import render,get_object_or_404
from .models import Question,Choice
from django.urls import reverse
from django.views import generic
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
# def detail(request,id):
#     question = get_object_or_404(Question, pk=id)
#     return render(request, "polls/detail.html", {'question':question})
# def results(request,question_id):
#     question=get_object_or_404(Question,pk=question_id)
#     return render(request,'polls/results.html',{'question':question})
def vote(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
        print(request.POST['choice'])
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except(KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{'question':question,'erro_message':'You did not select a choice'})
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question_id,)))
# def index(request):
#     latest_question_list=Question.objects.order_by('-pub_date')[:5]
#     context={'latest_question_list':latest_question_list}
#     return render(request,'polls/index.html',context)
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'
    model = Question
class ResultsView(generic.DetailView):
    template_name = 'polls/results.html'
    model = Question