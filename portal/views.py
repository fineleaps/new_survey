from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView
from .models import Survey, Question, Choice, Answer, Response
from django.http import Http404, HttpResponse
import uuid
from lazysignup.decorators import allow_lazy_user


@allow_lazy_user
def home(request):
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

@allow_lazy_user
def survey_start(request, slug):
    survey = get_object_or_404(Survey, slug=slug, active=True)
    if survey.has_questions:
        if request.method == "POST":
            Response.objects.get_or_create(user=request.user, survey=survey)
            post_dict = request.POST
            for ans in post_dict:
                if 'ans' in ans:
                    q_slug = ans[4:]
                    question = get_object_or_404(Question, slug=q_slug)
                    choice = get_object_or_404(Choice, slug=post_dict[ans])
                    Answer.objects.create(question=question, choice=choice, response=response)
            return redirect('survey_submitted')

        else:
            if not Response.objects.filter(user=request.user, survey=survey).exists():
                questions = survey.question_set.all()
                return render(request, 'portal/survey_start.html', {'questions': questions, 'survey': survey})
            else:
                return redirect('survey_already_done', slug=slug)
    else:
        return HttpResponse('Survey has no question')


# def survey_start(request, slug):
#     survey = get_object_or_404(Survey, slug=slug, active=True)
#     if survey.has_questions:
#         if request.method == "POST":
#             pass
#             # form = ResponseForm(request.POST)
#             # if form.is_valid():
#             #     form.save()
#         else:
#             if not Response.objects.filter(user=request.user, survey=survey).exists():
#                 response = Response.objects.create(user=request.user, survey=survey)
#                 response.answer_set.bulk_create((Answer(question=question, response=response) for question in survey.question_set.all()))
#                 return HttpResponse(response.id)
#             else:
#                 return redirect('survey_already_done', slug=slug)
#     return HttpResponse('Survey has no question')

@allow_lazy_user
def survey_already_done(request, slug):
    survey = get_object_or_404(Survey, slug=slug, active=True)
    return render(request, 'portal/survey_already_done.html', {'survey': survey})
