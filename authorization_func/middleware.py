from django.utils.functional import SimpleLazyObject
from rest_framework.authtoken.models import Token

class BearerTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        def get_user_token():
            if request.user.is_authenticated:
                try:
                    token = Token.objects.get(user=request.user)
                    return f"Bearer {token.key}"
                except Token.DoesNotExist:
                    pass
            return None

        user_token = SimpleLazyObject(get_user_token)
        authorization_header = request.META.get('HTTP_AUTHORIZATION')

        if user_token is not None:
            if authorization_header and 'Bearer' in authorization_header:
                parts = authorization_header.split()
                if len(parts) == 2 and parts[0].lower() == 'bearer':
                    user_token = f"Bearer {parts[1]}"
                else:
                    user_token = None
            else:
                user_token = None

        if user_token is not None:
            request.META['HTTP_AUTHORIZATION'] = user_token

        response = self.get_response(request)

        return response
