from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class HomeView(TemplateView):
    template_name = 'home.html'


login = LoginView.as_view(template_name='registration/login.html')
logout = LogoutView.as_view(next_page='/')
register = RegisterView.as_view()
home = HomeView.as_view()
