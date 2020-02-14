from rest_framework import permissions
from .models import *

class AllowMeetCreator(permissions.BasePermission):
    message = "You are not authorized to perform this task"

    def has_object_permission(self, request, view, obj):
        meetups = Meetup.objects.filter(pk=obj.id)
        if request.user.pk not in meetups.values_list('creator', flat=True):
            return False
        return True


class AllowMeetCreatorandMembers(permissions.BasePermission):
    message = "You are not authorized to perform this task"

    def has_object_permission(self, request, view, obj):
        meetups = Meetup.objects.filter(pk=obj.id)
        if request.user.pk not in meetups.values_list('creator', flat=True) and request.user.pk not in meetups.values_list('members', flat=True):
            return False
        return True