from django.db import models
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Max


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
    def get_instructions(self):
        return self.instructions.split('\n')

    @property
    def get_question_html_ids(self):
        return [str(qid) for qid in self.question_set.all().values_list('serial_number', flat=True)]

    @property
    def get_highest_html_id(self):
        return "question_" + str(self.question_set.all().order_by('serial_number').last().serial_number)

    @property
    def get_lowest_html_id(self):
        return "question_" + str(self.question_set.all().order_by('serial_number').first().serial_number)

    @property
    def get_question_wise_report(self):
        report_dict = {}
        for question in self.question_set.all():
            mini_dict = {}
            for choice in question.choice_set.all():
                mini_dict[choice] = Answer.objects.filter(choice=choice).count()
            report_dict[question] = mini_dict
        return report_dict

    @property
    def get_success_percentage(self):
        pn_questions = self.question_set.filter(possitive_or_negative=True)
        obt = sum([q.get_possitive_response for q in pn_questions])
        total = pn_questions.count()*100
        return float((obt/total)*100)

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
    possitive_or_negative = models.BooleanField(default=True)
    rating_type = models.BooleanField(default=False)
    choice_unit = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return self.question_text
    #
    # @property
    # def get_chart_choice_labels(self):
    #     print(type([choice.choice_text for choice in self.choice_set.all()]))
    #     return [str(choice.choice_text) for choice in self.choice_set.all()]

    @property
    def display_link(self):
        return "View"

    @property
    def get_total_votes(self):
        return Response.objects.filter(answer__question=self).count()

    @property
    def get_response_average(self):
        if self.possitive_or_negative:
            return Answer.objects.filter(question=self).aggregate(Avg('choice__possitive_count'))['choice__possitive_count__avg']

    @property
    def get_possitive_response(self):
        if self.possitive_or_negative:
            av = Answer.objects.filter(question=self).aggregate(Avg('choice__possitive_count'))['choice__possitive_count__avg']
            ma = Answer.objects.filter(question=self).aggregate(Max('choice__possitive_count'))['choice__possitive_count__max']
            return (av/ma)*100


def add_q_slug(sender, instance, *args, **kwargs):
    unique_text = instance.question_text[-5:] + str(instance.serial_number) + str(instance.id)
    if instance.slug != slugify(unique_text):
        instance.slug = slugify(unique_text)
        instance.save()


post_save.connect(add_q_slug, sender=Question)

possitive_count_class = ('#d9534f', '#FF8C00', '#FFD700', '#5bc0de', '#5cb85c')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=32)
    slug = models.SlugField(blank=True)
    chart_text = models.CharField(max_length=12, blank=True)
    serial_number = models.PositiveSmallIntegerField()
    possitive_count = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.question.question_text, self.choice_text)

    @property
    def get_rating_tag(self):
        if self.question.rating_type:
            return "star"

    @property
    def get_possitive_color(self):
        return possitive_count_class[self.possitive_count-1]

    @property
    def get_name_with_unit(self):
        return self.choice_text + self.question.choice_unit


def add_c_slug(sender, instance, *args, **kwargs):
    unique_text = instance.choice_text[-2:] + str(instance.question.slug) + str(instance.id)
    if instance.slug != slugify(unique_text):
        instance.slug = slugify(unique_text)
        instance.save()
    if not instance.chart_text:
        instance.chart_text = instance.choice_text[:12]
        instance.save()
    if not instance.possitive_count:
        instance.possitive_count = instance.serial_number
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
    user_feedback = models.TextField(blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        unique_together = ('user', 'survey')
