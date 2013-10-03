from registration.backends.simple.views import RegistrationView

class RegistrationRedirect(RegistrationView):
    def get_success_url(self, request, user):
        return "/"