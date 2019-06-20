from django.urls import include, path
from .views import main, workers, admins
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", main.home, name='home'),
    path('workers/', include(([
        path('', workers.dash, name='dash'),
        path('view_annotations', workers.view_annotations, name='view_annotations'),
        path('view_jobs', workers.view_jobs, name='view_jobs'),
        path('jobs/<job_id>', workers.jobs, name="jobs")
    ], 'main'), namespace='workers')),
    path('admins/', include(([
        path('', admins.panel, name='panel'),
        path('job/add/', admins.JobCreateView.as_view(), name="create_job"),
        path('job/update/<int:pk>', admins.JobUpdateView.as_view(), name='update_job'),
        path('job/delete/<int:pk>', admins.JobDeleteView.as_view(), name='delete_job'),
        path('batch/start/', admins.BatchCreateView.as_view(), name="start_batch"),
        path('batches', admins.view_batches, name="view_batches"),
        path('update_batch/<batch_id>', admins.update_batch, name="update_batch"),
        path('manage_workers', admins.manage_workers, name="manage_workers")
    ], 'main'), namespace='admins')),

]


if settings.DEBUG: #development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
