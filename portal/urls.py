from django.conf.urls import url
from django.views.generic import TemplateView
from . import views


urlpatterns = [

    # url(r'^$', views.TemplateView.as_view(template_name='portal/check_temp.html'), name='home'),
    url(r'^$', views.home, name='home'),
    url('survey/details/(?P<slug>[\w-]+)/$', views.SurveyDetailView.as_view(), name='survey_detail'),
    url('survey/start/(?P<slug>[\w-]+)/$', views.survey_start, name='survey_start'),
    url('survey/submitted/', TemplateView.as_view(template_name='portal/survey_submitted.html'), name='survey_submitted'),
    url('survey/already_given/(?P<slug>[\w-]+)/$', views.survey_already_done, name='survey_already_done'),

]
