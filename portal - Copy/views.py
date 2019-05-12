from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView
from .models import Survey, Question, Choice, Answer, MySession
from django.http import Http404, HttpResponse
import uuid


def get_or_create_session(request):
    s_id = request.session.get('my_session_id', None)
    if s_id is None:
        m_session = MySession.objects.create()
        request.session['my_session_id'] = m_session.id
    else:
        m_session = MySession.objects.get(id=s_id)
    return m_session


class HomeView(TemplateView):
    template_name = 'portal/home.html'

    def get_context_data(self, **kwargs):
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
                Answer.objects.create(question=question, choice=choice, my_session=get_or_create_session(request))
        return redirect('survey_submitted')

    else:
        answer_set = Answer.objects.filter(my_session=get_or_create_session(request), question__survey=survey)
        if answer_set.exists():
            return redirect('survey_already_done', slug=slug)
        else:
            questions = survey.question_set.all()
            return render(request, 'portal/survey_start.html', {'questions': questions, 'survey': survey})


def survey_already_done(request, slug):
    survey = get_object_or_404(Survey, slug=slug, active=True)
    return render(request, 'portal/survey_already_done.html', {'survey': survey})
