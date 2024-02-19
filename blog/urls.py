from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
#from .views import signup, user_login, user_logout
# app_name = "blog"
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/', views.tag_list, name='tag_list'),
    path('signup/', views.signup, name='signup'),
    path('login/',views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('post/', views.post_new, name='post_new'),
    path('category/', views.category_list, name='category_list'),
    path('tag/<slug:slug>/', views.tag_post, name='tag_post'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('user/<int:user_id>/edit/', views.edit_profile, name='edit_profile'),
    path('post/<int:post_id>/comments/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_post, name='category_post'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
   
    ]
