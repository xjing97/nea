from django.db import models


class UserDepartmentManager(models.Manager):
    pass


class UserDepartment(models.Model):
    department_name = models.CharField(max_length=256, default="", unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = UserDepartmentManager()

    def __str__(self):
        return self.department_name


class GRC(models.Model):
    user_department = models.ForeignKey(UserDepartment, on_delete=models.PROTECT, related_name='grc')
    grc_name = models.CharField(max_length=256, default="NA")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

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
