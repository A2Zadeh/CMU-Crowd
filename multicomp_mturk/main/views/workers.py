from django.contrib.auth import login
from django.shortcuts import redirect,render
from django.views.generic import CreateView
from main.models import User,Job,Annotation,Batch,Worker
from ..forms import WorkerSignUpForm
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
  active_jobs = Job.objects.all()
  #pdb.set_trace()
  return render(request,'main/workers/dash.html',{'jobs':active_jobs})

def jobs(request,job_id):
    #active_jobs = Job.objects.all()
    job = Job.objects.get(id=job_id)
    #get batch here, should be oldest batch not completed && cancelled
    if request.method == 'POST':
        #FOR NOW, just taking the latest batch for this job!
        current_batch = Batch.objects.filter(job=job).last()
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
        #pdb.set_trace()
    else:
        template_url = job.html_template.url
        render_url = template_url.replace("/media/",'') #remove /media/ prefix
        #render_url="job_templates/test_form.html"
        context = {"hello":"Hello world"}
        return render(request,render_url,context)