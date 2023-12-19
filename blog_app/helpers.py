from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


def create_common_user_group():
    try:
        common_user_group = Group.objects.get(name='Common User')
    except Group.DoesNotExist:
        common_user_group = Group.objects.create(name='Common User')

        permissions = Permission.objects.filter(content_type__app_label='app_label_here')
        common_user_group.permissions.set(permissions)

    return common_user_group
