from rest_framework import permissions


class OwnAccount(permissions.BasePermission):

    def has_permission(self, request, view):
        return view.kwargs.get('user_id') == request.user.id
