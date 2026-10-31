from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError

class NoSignupAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False

    def signup(self, request, user, form):
        raise ValidationError("Самостоятельная регистрация на сервисе запрещена. Аккаунты создаются только администратором завода.")
