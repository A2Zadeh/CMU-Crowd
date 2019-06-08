from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect,render
from django.views.generic import CreateView
from main.models import User,Job,Admin,Batch
from ..forms import AdminSignUpForm

import pdb

class AdminSignUpView(CreateView):
    model = User
    form_class = AdminSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('home')

def panel(request):
  return render(request,'main/admins/panel.html')

class JobCreateView(CreateView):
    model = Job
    fields = ('title','description','hourly_pay','html_template',)
    template_name = 'main/admins/create_job_form.html'

    def form_valid(self,form):
        job = form.save(commit=True)
        admin = Admin.objects.get(user=self.request.user)
        job.admins.add(admin)
        job.save()
        messages.success(self.request,"Job created successfully.")
        return redirect('admins:panel')

class BatchCreateView(CreateView):
    model = Batch
    fields = ('job','content','num_HITs')
    template_name = "main/admins/create_batch_form.html"

    def form_valid(self,form):
        batch = form.save(commit=True)
        messages.success(self.request,"Batch created successfully.")
        return redirect('admins:panel')
    #pass

def view_batches(request):
    admin = Admin.objects.get(user=request.user)
    admin_jobs = admin.job_set.all()
    admin_batches = dict()
    for j in admin_jobs:
        admin_batches[j.title] = list(Batch.objects.filter(job=j))
    context = {'batches':admin_batches}
    #pdb.set_trace()
    return render(request,'main/admins/view_batches.html',context)




