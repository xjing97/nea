from django.core.management import BaseCommand

from department.models import UserDepartment, GRC, Division


class Command(BaseCommand):
    def handle(self, **args):
        user_department, created = UserDepartment.objects.get_or_create(department_name='Central Regional Office')
        grc, created = GRC.objects.get_or_create(grc_name='NA', user_department=user_department)
        Division.objects.get_or_create(division_name='NA', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Ang Mo Kio GRC', user_department=user_department)
        Division.objects.get_or_create(division_name='Ang Mo Kio-Hougang', grc=grc)
        Division.objects.get_or_create(division_name='Cheng San-Seletar', grc=grc)
        Division.objects.get_or_create(division_name='Jalan Kayu', grc=grc)
        Division.objects.get_or_create(division_name='Teck Ghee', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Kebun Baru SMC', user_department=user_department)
        Division.objects.get_or_create(division_name='Kebun Baru', grc=grc)

        grc, created = GRC.objects.get_or_create(grc_name='Yio Chu Kang SMC', user_department=user_department)
        Division.objects.get_or_create(division_name='Yio Chu Kang', grc=grc)


        # ERO
        user_department, created = UserDepartment.objects.get_or_create(department_name='Eastern Regional Office')
        grc, created = GRC.objects.get_or_create(grc_name='NA', user_department=user_department)
        Division.objects.get_or_create(division_name='NA', grc=grc)

        # WRO
        user_department, created = UserDepartment.objects.get_or_create(department_name='Western Regional Office')
        grc, created = GRC.objects.get_or_create(grc_name='NA', user_department=user_department)
        Division.objects.get_or_create(division_name='NA', grc=grc)

        # VCOD
        user_department, created = UserDepartment.objects.get_or_create(department_name='Vector Control Operation Division')
        grc, created = GRC.objects.get_or_create(grc_name='NA', user_department=user_department)
        Division.objects.get_or_create(division_name='NA', grc=grc)

        # SACD
        user_department, created = UserDepartment.objects.get_or_create(department_name='Sanitation and Compliance Division')
        grc, created = GRC.objects.get_or_create(grc_name='NA', user_department=user_department)
        Division.objects.get_or_create(division_name='NA', grc=grc)

        # SEI
        user_department, created = UserDepartment.objects.get_or_create(department_name='Singapore Environment Institute')
        grc, created = GRC.objects.get_or_create(grc_name='NA', user_department=user_department)
        Division.objects.get_or_create(division_name='NA', grc=grc)
