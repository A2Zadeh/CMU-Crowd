from django.urls import include, path
from .views import main, workers, admins
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
 path('',main.home,name='home'),
 path('workers/', include(([
        path('', workers.dash, name='dash'),
        path('jobs/<job_id>',workers.jobs,name="jobs")
    ], 'main'), namespace='workers')),
 path('admins/', include(([
        path('', admins.panel, name='panel'),
        path('job/add/',admins.JobCreateView.as_view(),name="create_job"),
        path('batch/start/',admins.BatchCreateView.as_view(),name="start_batch"),
        path('batches',admins.view_batches,name="view_batches"),
    ], 'main'), namespace='admins')),

]


if settings.DEBUG: #development
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
