from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from main.models import User
from ..forms import AdminSignUpForm

class AdminSignUpView(CreateView):
    model = User
    form_class = AdminSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('login')

