from django.db import models
from django.contrib.auth.models import AbstractUser


#MARK: User Models 
class User(AbstractUser):
  is_worker = models.BooleanField(default=False)
  is_admin = models.BooleanField(default=False)

#Admin  #1-to-1 with user
class Admin(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


#Worker #1-to-1 with user 
class Worker(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  time_worked = models.IntegerField(default=0)
  is_approved = models.BooleanField(default=False)  
  ##TODO: manually approve worker for each job, worker has a list of approved jobs (job ids)
  ##TODO: statistics of jobs done fields?



#Job 
class Job(models.Model):
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)
  title = models.CharField(max_length=255)
  description = models.TextField()
  hourly_pay = models.DecimalField(decimal_places=2, max_digits=5)
  admins = models.ManyToManyField(Admin)
  html_template = models.FileField(upload_to="job_templates")
  #TODO: image for job 
  #content = models.TextField()

  def __str__(self):
    return self.title

class Batch(models.Model):
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)
  job = models.ForeignKey(Job,on_delete=models.PROTECT)
  content = models.TextField()
  num_HITs = models.IntegerField(default=10)
  is_completed = models.BooleanField(default=False)
  is_cancelled = models.BooleanField(default=False)

class Annotation(models.Model):
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)
  worker = models.ForeignKey(Worker,null=True,on_delete=models.SET_NULL)
  batch = models.ForeignKey(Batch,on_delete=models.PROTECT)
  content = models.TextField()
  #TODO: time tracking for how long annotation took

#Log