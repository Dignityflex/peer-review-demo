from django.contrib import admin
from django.urls import path, include
from portal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
    path('', views.paper_list, name='paper_list'),
    path('paper/<int:pk>/', views.paper_detail, name='paper_detail'),
    path('submit/', views.submit_paper, name='submit_paper'),
    
]

