from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
  template_name = 'registration/sign_up.html'