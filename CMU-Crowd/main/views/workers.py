from django.contrib.auth import login
from django.shortcuts import redirect,render
from django.views.generic import CreateView
from main.models import User,Job,Annotation,Batch,Worker
from ..forms import WorkerSignUpForm
from django.template import Context, Template
from django.conf import settings
import json
import pdb

class WorkerSignUpView(CreateView):
    model = User
    form_class = WorkerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'worker'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('accounts/login')


def dash(request):
    #TODO: jobs that have one or more active batches
  active_jobs = Job.objects.all()
  worker = Worker.objects.get(user=request.user)
  work_done = Annotation.objects.filter(worker=worker).count()
  last_job_done  = Annotation.objects.filter(worker=worker).last().batch.job
  context = {'jobs':active_jobs,
                    'work_done':work_done,
                    'last_job': last_job_done,
                    'admin_email':settings.CONTACT_EMAIL
                    }
  #pdb.set_trace()
  return render(request,'main/workers/dash.html',context)


def view_jobs(request):
    worker = Worker.objects.get(user=request.user)
    jobs = Job.objects.all() #change to only approved jobs later 
    context = {"jobs":jobs}
    return render(request,'main/workers/view_jobs.html',context)

def view_annotations(request):
    worker = Worker.objects.get(user=request.user)
    annotations = Annotation.objects.filter(worker=worker)
    context = {"annotations":annotations}
    return render(request,'main/workers/view_annotations.html',context)

def jobs(request,job_id):
    #active_jobs = Job.objects.all()
    job = Job.objects.get(id=job_id)
    template_url = job.html_template.url
    render_url = template_url.replace("/media/",'') #remove /media/ prefix
    context = {}
    #get batch here, should be oldest batch not completed && cancelled
    if request.method == 'POST':
        #FOR NOW, just taking the first batch for job!
        current_batch = Batch.objects.filter(job=job).first()
        #pdb.set_trace()
        content_dict = {k: v for k, v in request.POST.items() 
        if k != 'csrfmiddlewaretoken'} #remove csrftoken
        #Create annotation object 
        worker = Worker.objects.get(user=request.user) #TODO: error handling
        Annotation.objects.create(
            worker=worker,
            batch = current_batch,
            content=json.dumps(content_dict),
            )
        #context = {"hello":"Hello world"}
        return render(request,render_url,context)
    #TODO: ++ TO BATCH NUM COMPLETED HERE 
    else:
        
        #pdb.set_trace()
        template = Template(job.html_template.read())
        
        #context  = {}
        #context = {"hello":"Hello world"}
        return render(request,render_url,context)