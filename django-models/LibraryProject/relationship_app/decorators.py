from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from functools import wraps


def role_required(role_name):
    """
    Decorator to check if user has the required role
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You must be logged in to access this page.")

            if hasattr(request.user, 'profile') and request.user.profile.role == role_name:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You don't have permission to access this page.")

        return _wrapped_view

    return decorator


# Specific role decorators
def admin_required(view_func):
    return role_required('admin')(view_func)


def librarian_required(view_func):
    return role_required('librarian')(view_func)


def member_required(view_func):
    return role_required('member')(view_func)


# User test functions for user_passes_test decorator
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'admin'


def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'librarian'


def is_member(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'member'
