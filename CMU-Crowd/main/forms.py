import json
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from main.models import Worker, Admin, User, Job, Batch


class WorkerSignUpForm(UserCreationForm):

  class Meta(UserCreationForm.Meta):
        model = User

        @transaction.atomic #ensures sent in 1 transaction
        def save(self):
            user = super().save(commit=False)
            user.is_worker = True
            user.save()
            worker = Worker.objects.create(user=user)
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
            return user

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('title', 'description', 'hourly_pay', 'html_template')

class BatchForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea,required=False)

    class Meta:
        model = Batch
        fields = ('job', 'content', 'num_HITs')
        #validation
    def clean_content(self):
        data = self.cleaned_data['content']
        if data != "": #some content provided
            try:
                json.loads(data)
            except:
                raise forms.ValidationError("Please enter a valid JSON.")
        return data
