from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login', views.login, name='login'),
    path('logout', views.log_out, name='logout'),
    path('register', views.register, name='register'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('create_post/', views.create_post, name= 'create_post'),
    path('post/<slug:slug>/edit', views.edit_blog, name='edit_blog'),
    path('post/<slug:slug>/delete', views.delete_blog, name='delete_blog'),
    
]
