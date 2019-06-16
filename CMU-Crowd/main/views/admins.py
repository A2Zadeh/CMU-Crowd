from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect,render,get_object_or_404
from django.views.generic import CreateView,UpdateView
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
    template_name = 'main/admins/create_job.html'

    def form_valid(self,form):
        job = form.save(commit=True)
        admin = Admin.objects.get(user=self.request.user)
        job.admins.add(admin)
        job.save()
        messages.success(self.request,"Job created successfully.")
        return redirect('admins:panel')

@method_decorator([login_required, admin_required], name='dispatch')
class JobUpdateView(UpdateView):
    model = Job
    fields = ('title','description','hourly_pay','html_template',)
    template_name = 'main/admins/update_job.html'

    def form_valid(self,form):
        job = form.save(commit=True)
        job.save()
        messages.success(self.request,"Job updated successfully.")
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

#have a cancel batch function,only POST
@login_required
@admin_required
def update_batch(request,batch_id):
    #pdb.set_trace()
    batch = get_object_or_404(Batch,id=batch_id)
    action = request.POST.get('action')
    if action == 'cancel':
        batch.is_cancelled = True
    elif action == 'restart':
        batch.is_cancelled = False
    batch.save()
    return redirect('admins:view_batches')




#have a restart batch function, only POST

#these both redirect back to view_batches


@login_required
@admin_required
def view_batches(request):

    def batch_status_class(batch):
        if batch.is_cancelled:
            return 'danger'
        elif batch.is_completed:
            return 'success'
        else: #active batch
            return 'primary'
    def batch_statistics(batch):
        stats = dict()
        stats['id'] = batch.id
        stats['num_HITs'] = batch.num_HITs
        stats['created_date'] = batch.created_date
        num_completed = Annotation.objects.filter(batch=batch).count()
        stats['percent_completion'] = (num_completed / batch.num_HITs) * 100
        stats['cancelled'] = batch.is_cancelled
        stats['completed'] = batch.is_completed
        stats['status_class'] = batch_status_class(batch)
        return stats 


    admin = Admin.objects.get(user=request.user)
    admin_jobs = admin.job_set.all()
    admin_batches = dict()
    jobs = dict()
    if request.POST:
        # action = request.POST.get('action')
        # batch_id = request.POST.get('batch_id')
        # batch = get_object_or_404(Batch,id=batch_id)
        # pdb.set_trace()
        # if action == 'cancel':
        #     batch.is_cancelled = True
        # elif action == 'restart':
        #     batch.is_cancelled = False
        # batch.save()
        pass
        #pdb.set_trace()
    else:
        pass
    for j in admin_jobs:
        batch_stats = [batch_statistics(b) for b in Batch.objects.filter(job=j)]
        admin_batches[j.title] = batch_stats
        jobs [j.title] = j.id

    context = {'batches':admin_batches,'jobs':jobs}
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


