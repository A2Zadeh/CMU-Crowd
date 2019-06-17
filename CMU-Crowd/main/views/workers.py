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
  context = {'jobs':active_jobs,
                    'work_done':work_done,
                    'last_job': None,
                    'admin_email':settings.CONTACT_EMAIL
                    }
  if work_done > 0:
    last_job_done  = Annotation.objects.filter(worker=worker).last().batch.job
    context['last_job'] = last_job_done
 
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

def batches_complete(job):
    batches = Batch.objects.filter(job=job)
    done = [b.is_completed or b.is_cancelled for b in batches]
    return all(done)


def jobs(request,job_id):
    job = Job.objects.get(id=job_id)
    if batches_complete(job):
        return render(request,'main/workers/job_complete.html')
        #return redirect('workers:job_complete')

    template_url = job.html_template.url
    render_url = template_url.replace("/media/","") #remove /media/ prefix
    #oldest batch not completed && cancelled
    current_batch = Batch.objects.filter(job=job).filter(is_completed=False).filter(is_cancelled=False).first()
    batch_content = json.loads(current_batch.content)
    if request.method == 'POST':
        content_dict = {k: v for k, v in request.POST.items() 
        if k != 'csrfmiddlewaretoken'} #remove csrftoken
        #Create annotation object 
        worker = Worker.objects.get(user=request.user) 

        #TODO: error handling
        Annotation.objects.create(
            worker=worker,
            batch = current_batch,
            batch_content_index= current_batch.num_completed,
            content=json.dumps(content_dict),
            )
        current_batch.num_completed += 1
        current_batch.save()
        if current_batch.num_completed == current_batch.num_HITs:
            current_batch.is_completed = True
            current_batch.save()
        #context = {"hello":"Hello world"}
        context = batch_content[current_batch.num_completed]
        return render(request,render_url,context)
    else:
        #template = Template(job.html_template.read())
        #batch = Batch.objects.filter(job=job).filter(cancelled=False).filter(completed=False).first()
        context = batch_content[current_batch.num_completed]
        return render(request,render_url,context)