from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from main.models import Worker,Admin,User,Job


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


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

class JobForm(BaseForm):
  class Meta:
    model = Job
    fields = ('title','description','hourly_pay','html_template')
    # widgets = {
    #    'title': forms.TextInput(attrs={'class': 'form-control'}),
    #    'description': forms.TextInput(attrs={'class': 'form-control'})
    # }
    #todo: validation here