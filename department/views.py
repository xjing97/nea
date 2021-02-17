from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from department.models import UserDepartment, GRC, Division


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_user_department(request):
    user_department = UserDepartment.objects.values(
        'id', 'department_name', 'grc__id', 'grc__grc_name', 'grc__division__id', 'grc__division__division_name')

    return Response(data={'data': list(user_department)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_department(request):
    user_department_id = request.GET.get('user_department_id', '')
    user_department = UserDepartment.objects.filter(id=user_department_id).first()

    if not user_department:
        return Response(status=400, data='User department does not exists')

    return Response(data={'user_department_name': user_department.department_name,
                          'user_department_id': user_department_id})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_user_department(request):
    user_department_name = request.data.get('name', '')

    if not user_department_name:
        return Response(status=400, data='User department name is required')

    user_department, created = UserDepartment.objects.get_or_create(department_name=user_department_name)

    if not created:
        return Response(status=400, data='%s already exists' % user_department.department_name)

    return Response(data={'user_department_name': user_department.department_name, 'user_department_id': user_department.id})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_user_department(request):
    user_department_id = request.data.get('id', '')
    user_department_name = request.data.get('name', '')
    user_department = UserDepartment.objects.filter(id=user_department_id).first()

    if not user_department:
        return Response(status=400, data='User department does not exist')

    user_department.name = user_department_name
    user_department.save()

    return Response(data={'user_department_name': user_department.department_name,
                          'user_department_id': user_department.id})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_division(request):
    user_department = Division.objects.values(
        'id', 'grc__user_department__department_name', 'grc__grc_name', 'division_name')

    return Response(data={'data': list(user_department)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_grc_by_department(request):
    if 'user_department_id' not in request.GET:
        return Response(status=400, data={'message': 'Required argument user_department_id is missing'})

    user_department_id = request.GET.get('user_department_id', '')

    user_department = UserDepartment.objects.filter(id=user_department_id).first()

    if not user_department:
        return Response(status=400, data={'message': 'User Department ID %s not found' % user_department_id})

    grc = GRC.objects.filter(user_department_id=user_department_id).values('id', 'grc_name')

    return Response(data={'data': {'grc': list(grc), 'user_department_name': user_department.department_name,
                                   'user_department_id': user_department_id}})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_grc(request):
    grc_id = request.GET.get('grc_id', '')
    grc = GRC.objects.filter(id=grc_id).first()

    if not grc:
        return Response(status=400, data='User department does not exists')

    user_departments = UserDepartment.objects.values('id', 'department_name')

    return Response(data={'user_departments': list(user_departments),
                          'user_department_id': grc.user_department.id,
                          'grc_name': grc.grc_name,
                          'grc_id': grc_id})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_grc(request):
    grc_name = request.data.get('name', '')
    user_department_id = request.data.get('user_department_id', '')

    if not grc_name:
        return Response(status=400, data='GRC name is required')

    if not user_department_id:
        return Response(status=400, data='User Department is required')

    grc, created = GRC.objects.get_or_create(grc_name=grc_name, user_department_id=user_department_id)

    if not created:
        return Response(status=400, data='%s already exists' % grc.grc_name)

    return Response(data={'grc_name': grc.grc_name, 'grc_id': grc.id})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_grc(request):
    grc_id = request.data.get('id', '')
    grc_name = request.data.get('name', '')
    user_department_id = request.data.get('user_department_id', '')
    grc = GRC.objects.filter(id=grc_id).first()

    if not grc:
        return Response(status=400, data='GRC does not exist')

    user_department = UserDepartment.objects.filter(id=user_department_id).first()

    if not user_department:
        return Response(status=400, data='User department does not exist')

    grc.name = grc_name
    grc.user_department = user_department
    grc.save()

    return Response(data={'grc_name': grc.grc_name, 'grc_id': grc.id})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_division_by_grc(request):
    if 'grc_id' not in request.GET:
        return Response(status=400, data={'message': 'Required argument grc_id is missing'})

    grc_id = request.GET.get('grc_id', '')

    grc = GRC.objects.filter(id=grc_id).first()

    if not grc:
        return Response(status=400, data={'message': 'GRC ID %s not found' % grc_id})

    divisions = Division.objects.filter(grc_id=grc_id).values('id', 'division_name')

    return Response(data={'data': {'divisions': list(divisions), 'grc_id': grc.id, 'grc_name': grc.name,
                                   'user_department_name': grc.user_department.department_name,
                                   'user_department_id': grc.user_department.id}})

