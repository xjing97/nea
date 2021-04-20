from django.db import models
from django.db.models import Avg, Case, When, F, Count, IntegerField, Q


class UserDepartmentManager(models.Manager):
    pass


class UserDepartment(models.Model):
    department_name = models.CharField(max_length=256, default="", unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = UserDepartmentManager()

    def __str__(self):
        return self.department_name


class GRCManager(models.Manager):
    def get_average_scores_by_scenario(self, from_date=None, to_date=None, last_attempt_ids=[]):
        q = Q(division__user__is_active=True)
        if from_date:
            q &= Q(division__user__result__dateCreated__gte=from_date)
        if to_date:
            q &= Q(division__user__result__dateCreated__lte=to_date)

        if last_attempt_ids:
            q &= Q(division__user__result__id__in=last_attempt_ids)

        average_scores = GRC.objects.filter(q).values('grc_name').annotate(
            module=F('division__user__result__scenario__module__module_name'),
            average=Avg(F('division__user__result__results'))
        )
        return average_scores

    def get_passing_rate_of_grcs(self, from_date=None, to_date=None, last_attempt_ids=[]):
        q = Q(division__user__is_active=True)
        if from_date:
            q &= Q(division__user__result__dateCreated__gte=from_date)
        if to_date:
            q &= Q(division__user__result__dateCreated__lte=to_date)

        if last_attempt_ids:
            q &= Q(division__user__result__id__in=last_attempt_ids)

        passing_rates = GRC.objects.filter(q).values('grc_name').annotate(
            passed=Count(Case(When(division__user__result__is_pass=True, then=1), output_field=IntegerField())),
            failed=Count(Case(When(division__user__result__is_pass=False, then=1), output_field=IntegerField())),
        )

        return passing_rates


class GRC(models.Model):
    user_department = models.ForeignKey(UserDepartment, on_delete=models.PROTECT, related_name='grc')
    grc_name = models.CharField(max_length=256, default="NA")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = GRCManager()

    class Meta:
        unique_together = ['user_department', 'grc_name']

    def __str__(self):
        return self.grc_name


class Division(models.Model):
    grc = models.ForeignKey(GRC, on_delete=models.PROTECT, related_name='division')
    division_name = models.CharField(max_length=256, default="NA")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['grc', 'division_name']

    def __str__(self):
        return self.division_name

    def delete_division(self):
        if self.user.filter(is_active=True):
            return "Failed to delete division. %s user(s) is assigned to this division" % \
                   str(self.user.filter(is_active=True).count())

        else:
            try:
                # removed inactive users' division
                self.user.filter(is_active=False, division=self).update(division=None)

                self.delete()

                return None

            except Exception as e:
                return str(e)
