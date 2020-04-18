import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic

from .models import Question, Choice


class IndexView(generic.ListView):
    """
    Class-based views are an alternative way to implement views as Python objects instead of functions.
    Since a view is a callable that takes a web request and returns a web response,
    you can also define your views as class methods.
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    choices = Choice.objects.order_by('-pub_date')[:5]
#    context = {
#        "latest_question_list": latest_question_list
#    }
#    #template = loader.get_template('polls/index.html')
#    #return HttpResponse(template.render(context, request))
#    return render(request, 'polls/index.html', context)
#
#
#def detail(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/detail.html', {'question': question})
#
#
#def results(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # We are using the reverse() function in the HttpResponseRedirect constructor in this example.
        # This function helps avoid having to hardcode a URL in the view function.It is given the name of the
        # view that we want to pass control to and the variable portion of the URL pattern that points to that view.
        # In this case, using the URLconf we set up in Tutorial 3, this reverse() call will return a string like
        # /polls/3/results/
