from django.urls import path
from .import views

urlpatterns = [
    path('', views.registration),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('logout', views.logout),
    path('addnewjob', views.addnewjob),
    path('addjob', views.addjob),
    path('addtouser/<int:id>', views.addtouser),
    path('edit/<int:id>', views.edit),
    path('update/<int:id>', views.update),
    path('cancel/<int:id>', views.cancel),
    path('view/<int:id>', views.view),
    path('done/<int:id>', views.done)
]
