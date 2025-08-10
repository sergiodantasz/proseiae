from threading import local

_thread_locals = local()


def get_current_theme():
    return getattr(_thread_locals, "theme", "emerald")


def get_current_theme_colors():
    theme_colors = {
        "emerald": ("66cc8a", "223d30"),
        "night": ("3abdf8", "010d15"),
    }
    return theme_colors.get(get_current_theme(), theme_colors["emerald"])


class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.theme = request.COOKIES.get("theme", "emerald")
        response = self.get_response(request)
        return response
