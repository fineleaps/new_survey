from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView
from .models import Survey, Question, Choice, Answer, Response
from django.http import Http404, HttpResponse
import uuid
from lazysignup.decorators import allow_lazy_user
from django.contrib.auth.decorators import user_passes_test


def clear_session(request):
    request.session.clear()
    return redirect('home')


@allow_lazy_user
def home(request):
    return redirect('survey_detail', slug=Survey.objects.filter(active=True).first().slug)
    # surveys = Survey.objects.active()
    # return render(request, 'portal/home.html', {'surveys': surveys})


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


@allow_lazy_user
def survey_start(request, slug):
    survey = get_object_or_404(Survey, slug=slug, active=True)
    if survey.has_questions:
        if request.method == "POST":
            post_dict = request.POST
            response = Response.objects.get_or_create(user=request.user, survey=survey, user_feedback=post_dict['feedback'])[0]
            Answer.objects.bulk_create([Answer(question_id=int(ans[4:]), choice_id=int(post_dict[ans]), response=response) for ans in post_dict if 'ans' in ans])
            return redirect('survey_submitted')
        else:
            if not Response.objects.filter(user=request.user, survey=survey).exists():
                questions = survey.question_set.all()
                return render(request, 'portal/survey_start.html', {'questions': questions, 'survey': survey})
            else:
                return redirect('survey_already_done', slug=slug)
    else:
        return HttpResponse('Survey has no question')


@allow_lazy_user
def survey_already_done(request, slug):
    survey = get_object_or_404(Survey, slug=slug, active=True)
    return render(request, 'portal/survey_already_done.html', {'survey': survey})


@user_passes_test(lambda u: u.is_superuser)
def admin_home(request):
    surveys = Survey.objects.active()
    return render(request, 'my_admin/home.html', {'surveys': surveys})


@user_passes_test(lambda u: u.is_superuser)
def survey_report(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
