from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView
from .models import Survey, Question, Choice, Answer
from django.http import Http404, HttpResponse
from django.forms import formset_factory, modelformset_factory
from django.contrib import messages
from ipware import get_client_ip
import uuid
from ipware.ip import get_trusted_ip, get_ip, get_real_ip



def get_local_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class HomeView(TemplateView):
    template_name = 'portal/home.html'

    def get_context_data(self, **kwargs):
        if 'session_unique_f_id' not in self.request.session:
            self.request.session['session_unique_f_id'] = uuid.uuid3()
        context = super().get_context_data()
        context['surveys'] = Survey.objects.active()
        return context


def home(request):
    if 'session_unique_f_id' not in request.session:
        request.session['session_unique_f_id'] = uuid.uuid4()
    surveys = Survey.objects.active()
    return render(request, 'portal/home.html', {'surveys': surveys})



class SurveyDetailView(DetailView):
    template_name = 'portal/survey_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'survey'

    model = Survey

    def get_object(self, queryset=None):
        survey = super().get_object(queryset=queryset)
        if not survey.active:
            raise Http404('Invalid Request')
        return survey


def survey_start(request, slug):
    survey = get_object_or_404(Survey, slug=slug, active=True)
    if request.method == "POST":
        print('post ')
        post_dict = request.POST
        for ans in post_dict:
            if 'ans' in ans:
                q_slug = ans[4:]
                question = get_object_or_404(Question, slug=q_slug)
                choice = get_object_or_404(Choice, slug=post_dict[ans])
                Answer.objects.create(question=question, choice=choice, unique_id=request.COOKIES['sessionid'])
        return redirect('survey_submitted')

    else:
        answer_set = Answer.objects.filter(unique_id=request.COOKIES['sessionid'], question__survey=survey)
        if answer_set.exists():
            return redirect('survey_already_done', slug=slug)
        else:
            questions = survey.question_set.all()
            return render(request, 'portal/survey_start.html', {'questions': questions, 'survey': survey})


def survey_already_done(request, slug):
    survey = get_object_or_404(Survey, slug=slug, active=True)
    return render(request, 'portal/survey_already_done.html', {'survey': survey})
#     #
    # AnswerModelFormset = modelformset_factory(Answer, fields=('choice', ), extra=4)
    # formset = AnswerModelFormset(request.POST or None)
    # if formset.is_valid():
    #     formset.save()
    # context = {'formset': formset}
    # return render(request, 'portal/survey_start.html', context)
