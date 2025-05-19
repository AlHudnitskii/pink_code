from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import AccessToken

from core.auth_.models import User

class CustomIsAuthenticatedPermission(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return False

        try:
            token_str = auth_header.split()[1]
            token = AccessToken(token_str)
            user_id = token["user_id"]
            user_instance = User.objects.get(pk=user_id)
        except IndexError:
            raise AuthenticationFailed({"detail": "Неверный формат заголовка Authorization"})
        except KeyError:
            raise AuthenticationFailed({"detail": "Утверждение user_id не найдено в токене"})
        except AccessToken.VerifyTokenError:
            raise AuthenticationFailed({"detail": "Недействительный или истекший токен"})
        except User.DoesNotExist:
            raise AuthenticationFailed({"detail": "Пользователь не найден"})

        request.user = user_instance
        return True
    
class CustomIsAdminPermission(CustomIsAuthenticatedPermission):
    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if has_permission and request.user.is_staff:
            return True
        return False
