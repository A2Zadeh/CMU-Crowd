from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from main.models import Worker,Admin,User,Job

class WorkerSignUpForm(UserCreationForm):

  class Meta(UserCreationForm.Meta):
    model = User

  @transaction.atomic #ensures sent in 1 transaction
  def save(self):
    user = super().save(commit=False)
    user.is_worker = True
    user.save()
    worker = Worker.objects.create(user=user)
    #Note: save any fields to worker profile here.
    return user

class AdminSignUpForm(UserCreationForm):

  class Meta(UserCreationForm.Meta):
    model = User

  @transaction.atomic #ensures sent in 1 transaction
  def save(self):
    user = super().save(commit=False)
    user.is_admin = True
    user.save()
    worker = Admin.objects.create(user=user)
    #Note: save any fields to worker profile here.
    return user

class JobForm(forms.ModelForm):

  class Meta:
    model = Job
    fields = ('title','description','hourly_pay','html_template')

    #todo: validation here