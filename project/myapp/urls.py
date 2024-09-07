from django.urls import path, include
from . import views
from .views import signup, login_user, logout_user, start_vc, create

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('index', views.index, name='home'),
    path('signup', views.signup, name='signup'),
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('profile', views.profile, name='profile'),
    path('home', views.home, name='home'),
    path('create', views.create, name='create'),  # Page for creating a VC
    path('update', views.update, name='update'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('store_skills', views.store_skills, name='store_skills'),
    
    # Video Conference-related paths
    path('start_vc/', views.start_vc, name='start_vc'),  # This might be unnecessary since join_vc leads to start_vc.html
    path('join_vc/<int:vc_id>/', views.join_vc, name='join_vc'),  # View to join a VC
] 

# Serving media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
