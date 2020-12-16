from rest_framework.decorators import permission_classes


def permission_exempt(func):
    return permission_classes([])(func)
