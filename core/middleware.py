from threading import local

_thread_locals = local()


def get_current_theme():
    return getattr(_thread_locals, "theme", "emerald")


class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.theme = request.COOKIES.get("theme", "emerald")
        response = self.get_response(request)
        return response
