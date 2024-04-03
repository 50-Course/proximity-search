from rest_framework_api_key import permissions as api_key_permissions


class HasAPIKeyPermission(api_key_permissions.HasAPIKey):
    """
    Permission hook that checks if a request has a valid internal API key 
    for a given user.

    API Keys are generated for users and are used to authenticate requests
    """

    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)
