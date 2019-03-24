from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
  template_name = 'registration/sign_up.html'

def home(request):
  if request.user.is_authenticated:
    if request.user.is_admin:
      return redirect('admins:panel')
    else: #worker
      return redirect('workers:dash')
  return render(request,'main/home.html')