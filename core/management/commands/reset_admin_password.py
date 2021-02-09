from django.core.management import BaseCommand

from core.models import User


class Command(BaseCommand):
    def handle(self, **args):
        user = User.objects.filter(username='admin').first()
        user.set_password('admin123')
        user.save()
