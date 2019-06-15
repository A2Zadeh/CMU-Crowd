from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect,render
from django.views.generic import CreateView
from main.models import User,Job,Admin,Batch,Worker,Annotation
from ..forms import AdminSignUpForm
from ..decorators import admin_required

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

@login_required
@admin_required
def panel(request):
    admin = Admin.objects.get(user=request.user)

    context = {"active_job_count":Job.objects.filter(admins=admin).count() }
    return render(request,'main/admins/panel.html',context)




@method_decorator([login_required, admin_required], name='dispatch')
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


@method_decorator([login_required, admin_required], name='dispatch')
class BatchCreateView(CreateView):
    model = Batch
    fields = ('job','content','num_HITs')
    template_name = "main/admins/create_batch_form.html"

    def form_valid(self,form):
        batch = form.save(commit=True)
        messages.success(self.request,"Batch created successfully.")
        return redirect('admins:panel')
    #pass

@login_required
@admin_required
def view_batches(request):

    # def batch_status(batch):
    #     if batch.cancelled:
    #         #danger
    #     elif batch.completed:
    #         #success
    #     else:
    #         #primary
    def batch_data(batch):
        #num_completed = Annotation.objects.filter(batch=b).count()
        pass 


    admin = Admin.objects.get(user=request.user)
    admin_jobs = admin.job_set.all()
    admin_batches = dict()
    for j in admin_jobs:
        #admin_batches[j.title] = [batch_data(b) for b in Batch.objects.filter(job=j)]
        admin_batches[j.title] = list(Batch.objects.filter(job=j))

    context = {'batches':admin_batches}
    #pdb.set_trace()
    return render(request,'main/admins/view_batches.html',context)

@login_required
@admin_required
def manage_workers(request):
    def worker_statistics(worker):
        stats = dict()
        stats['id'] = worker.user.id
        stats['username'] = worker.user.username
        stats['date_joined'] = worker.user.date_joined
        stats['num_anns'] = Annotation.objects.filter(worker=worker).count()

        return stats


    workers = [worker_statistics(w) for w in Worker.objects.all()]
    context = {'workers':workers}


    return render(request,'main/admins/manage_workers.html',context)


