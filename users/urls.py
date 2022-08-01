from django.contrib.auth import logout
from django.urls import path
from . import views #linking views.py's functions to our views.url links

urlpatterns  = [
    path('', views.allprofiles, name = 'profiles_link'),
    path('profile/<str:pk>/', views.userprofile,  name = 'user_profile_link'),

    path('login/', views.loginfxn, name = 'loginlink'),
    path('logout/',  views.logoutfxn , name = 'logoutlink'),
    path('register/', views.registerfxn, name = 'registerlink'),

    path('useraccount/', views.userAccountfxn, name = 'useraccount'),
    path('edit_account/', views.editAccountfxn, name = 'edit_acct'),
    path('create_skill/', views.createSkill, name = 'create-skill'),
    path('update_skill/<str:pk>/', views.updateSkill, name = 'update-skill'),
    path('delete_skill/<str:pk>/', views.deleteSkill, name = 'delete-skill'),

    path('inbox/', views.inbox, name = 'inbox'), 
    path('message/<str:pk>/', views.viewMessage, name = 'read_message'),
    path('create-message/<str:pk>/', views.createMessage, name = 'create_message'), 

]
