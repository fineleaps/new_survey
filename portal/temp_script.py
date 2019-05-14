from portal.models import Question

for q in Question.objects.all():
    choices = q.choice_set.all()
    for i in range(1, q.choice_set.all().count()+1):
        choices = q.choice_set.all()
        ec = choices[i-1]
        ec.serial_number = list(choices)[-i].possitive_count
        ec.save()
