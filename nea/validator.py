from core.models import User


class ValidateIsAdmin(object):
    is_admin = False
    error_message = 'You do not have permission to perform this action.'

    def validate(self, user_id):
        user = User.objects.filter(id=user_id).first()
        if user.is_staff or user.is_superuser:
            self.is_admin = True
            self.error_message = ''
            return True

        return False
