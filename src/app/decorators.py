from django.shortcuts import redirect


def not_authorized(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main")
        return func(request, *args, **kwargs)
    return wrapper
