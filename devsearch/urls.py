"""devsearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 

#from projects.views import projects 

#coming fromour settings.py having configured the MEDIA_URL
from django.conf import settings
from django.conf.urls.static import static

#passwor reset 21-02-22 9:34
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
                   
    #created a urls py file in our projects and moved everything over there,,,to be linked here with the include key word above, and the url below
    path('', include('projects.urls')),
    path('users/', include('users.urls')),
    path('api/', include('api.urls')), #no import neccessary it seems

    #password reset urls:
    #1) User submits email for reset
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name = 'reset_password.html'), name = 'reset_password'),

    #2) Email sent message
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name ='reset_password_sent.html'), name = 'password_reset_done'),

    #3) link  and reset instructions within Email user clicks on to render form to be filled for pwd reset
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'new_password.html'), name = 'password_reset_confirm'),
    #       uidb64 encodes userID in a base 64 encryption

    #4) Password succesfully reset message
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'reset_password_complete.html'), name = 'password_reset_complete'),

]

#part two or MEDIA_URL config -- AFTER WHICH YOU CAN PLACE IT IN A TAG IN YOUR PROJECT SPECIFIC PAGES
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
 
