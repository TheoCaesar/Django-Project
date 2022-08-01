from django.urls import path

from . import views

urlpatterns = [
    path('', views.projectwork , name = 'homepage'), #creating a homepage
    path('product/', views.projects , name = 'products' ),      #it is by these names that we will later be creating hyperlinks...the django way
    path('services/', views.services , name = 'services'),
    #path('bespoke/<str:order>/', views.bespoke_services, name = 'bespoke'),
    path('bespoke/<str:pk>/' , views.project_WORK, name = 'projs'), 
    
    #10 - nov - 21 10:55am
    path('finalproj/', views.finalproj, name = 'fprojq'), #dont forget the url name goes into the hyperlinking
    path('finproj/<str:pk>/', views.finproj, name = 'fprojren'),
    path('create_project/' , views.create_proj, name = 'createproject'), 
    path('update_project/<str:pk>/', views.update_proj, name='updateproject'), 
    path('delete_proj/<str:pk>/', views.delete_proj, name = 'deleteproject')
]