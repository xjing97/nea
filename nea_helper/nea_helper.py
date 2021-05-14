from django.db.models import Func


class RoundWithPlaces(Func):
    function = 'ROUND'
