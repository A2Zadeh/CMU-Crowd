from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from main.models import Worker,Admin,User,Job,Batch
import json

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
          pass
            #field.widget.attrs['class'] = 'form-control'


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

class BatchForm(BaseForm):

  content = forms.CharField(widget=forms.Textarea,required=False)

  class Meta:
    model = Batch
    fields = ('job','content','num_HITs')
    #validation
  def clean_content(self):
    data = self.cleaned_data['content']
    if data != '': #no content provided
      try:
        json.loads(data)
      except:
        raise forms.ValidationError("Please enter a valid JSON.")
    return data

  # def clean(self):
  #   content = self.cleaned_data['content']
  #   num_HITs = self.cleaned_data['num_HITs']
  #   if len(json.loads(content)) != num_HITs:
  #     raise forms.ValidationError("JSON length is not the same as number of HITs.")