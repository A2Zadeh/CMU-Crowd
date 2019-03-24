from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from main.models import User
from ..forms import WorkerSignUpForm

class WorkerSignUpView(CreateView):
    model = User
    form_class = WorkerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'worker'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('login')

