from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import ChangePasswordSerializer
from core.models import User
from core.serializers import LoginSerializer
from nea.decorators import permission_exempt

from django.shortcuts import get_object_or_404


@api_view(['POST'])
@permission_exempt
def login(request):
    form = LoginSerializer(data=request.data)
    if not form.is_valid():
        return Response(status=400, data=form.errors)
    res = form.login(login_type='unity-api')
    return res


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj
