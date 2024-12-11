from django.conf import settings

class AdminSessionMiddleware:
    """
    Middleware para alternar os cookies de sessão entre admin e site público.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            # Usar cookie de sessão para o admin
            settings.SESSION_COOKIE_NAME = settings.ADMIN_SESSION_COOKIE_NAME
        else:
            # Usar cookie de sessão para o site público
            settings.SESSION_COOKIE_NAME = settings.SITE_SESSION_COOKIE_NAME
        return self.get_response(request)
