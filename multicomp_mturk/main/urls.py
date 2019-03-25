from django.urls import include, path

from .views import main, workers, admins

urlpatterns = [
 path('',main.home,name='home'),
 path('workers/', include(([
        path('', workers.dash, name='dash'),
    ], 'main'), namespace='workers')),
 path('admins/', include(([
        path('', admins.panel, name='panel'),
        path('job/add/',admins.JobCreateView.as_view(),name="create_job")
    ], 'main'), namespace='admins')),

]