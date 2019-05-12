from django.db import models
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User


class SurveyManager(models.Manager):

    def active(self):
        return super().filter(active=True)


class Survey(models.Model):
    name = models.CharField(max_length=32, unique=True)
    slug = models.SlugField(max_length=300, blank=True)
    purpose = models.TextField()
    instructions = models.TextField()
    active = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('survey_detail', kwargs={'slug': self.slug})

    @property
    def has_questions(self):
        return self.question_set.exists()

    @property
    def get_question_html_ids(self):
        return [str(qid) for qid in self.question_set.all().values_list('serial_number', flat=True)]

    @property
    def get_highest_html_id(self):
        return "question_" + str(self.question_set.all().order_by('serial_number').last().serial_number)

    @property
    def get_lowest_html_id(self):
        return "question_" + str(self.question_set.all().order_by('serial_number').first().serial_number)

    objects = SurveyManager()


def add_s_slug(sender, instance, *args, **kwargs):
    if instance.slug != slugify(instance.name):
        instance.slug = slugify(instance.name)
        instance.save()


pre_save.connect(add_s_slug, sender=Survey)


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=64)
    slug = models.SlugField(blank=True)
    serial_number = models.PositiveSmallIntegerField(default=30)

    # choice_unit = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return self.question_text

    @property
    def display_link(self):
        return "View"


def add_q_slug(sender, instance, *args, **kwargs):
    unique_text = instance.question_text[-5:] + str(instance.serial_number) + str(instance.id)
    if instance.slug != slugify(unique_text):
        instance.slug = slugify(unique_text)
        instance.save()


post_save.connect(add_q_slug, sender=Question)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=32)
    slug = models.SlugField(blank=True)
    serial_number = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return "{} - {}".format(self.question.question_text, self.choice_text)



def add_c_slug(sender, instance, *args, **kwargs):
    unique_text = instance.choice_text[-2:] + str(instance.question.slug) + str(instance.id)
    if instance.slug != slugify(unique_text):
        instance.slug = slugify(unique_text)
        instance.save()


post_save.connect(add_c_slug, sender=Choice)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    choice = models.ForeignKey(Choice, on_delete=models.PROTECT, blank=True, null=True)
    response = models.ForeignKey('Response', on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.choice)

    class Meta:
        unique_together = ('question', 'response')


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        unique_together = ('user', 'survey')
