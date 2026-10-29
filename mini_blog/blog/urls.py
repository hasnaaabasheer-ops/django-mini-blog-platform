from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path(
        'profile/',
        views.profile_view,
        name='profile'
    ),

    path(
        'post/new/',
        views.post_create,
        name='post_create'
    ),

    path(
        'post/<slug:slug>/',
        views.post_detail,
        name='post_detail'
    ),

    path(
        'post/<slug:slug>/edit/',
        views.post_edit,
        name='post_edit'
    ),

    path(
        'post/<slug:slug>/delete/',
        views.post_delete,
        name='post_delete'
    ),

    path(
        'comment/<int:pk>/delete/',
        views.comment_delete,
        name='comment_delete'
    ),

    path(
        'my-posts/',
        views.my_posts,
        name='my_posts'
    ),
]