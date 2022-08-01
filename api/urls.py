from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('', views.getRoutes),
    path('projects/', views.getProjects),
    path('projects/<str:pk>/', views.getProject),   #i did notice project(s)- but following dennis

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('projects/<str:pk>/vote/', views.projectVote),
]
#   nw we make our devsearch project aware of our api urls. so we include the api urls in the project's urls folder.
     