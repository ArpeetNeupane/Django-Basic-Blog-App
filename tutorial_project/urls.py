"""
URL configuration for tutorial_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views #as is used because multiple views can be imported so just giving a name
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', user_views.register, name = 'register'),
    path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name = 'login'), #login and logout are class based views, 
    #this built-in views will handle forms for us, we just have to make our template. by default it was looking for template for login in blog 
    #directory's template, but by passing argument, we made django look in users, as login is related to user we put it in that directory.
    path('logout/', user_views.logout_view, name = 'logout'),
    path('profile/', user_views.profile, name = 'profile'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name = 'users/password_change.html'), name = 'password_change'),
    #these pw related views are built-in views so no need to create new views
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name = 'users/password_change_done.html'), name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'users/password_reset.html'), name = 'password_reset'), #route for password reset
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'), name = 'password_reset_done'), #route after reset requested, telling users to check email
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'users/password_reset_confirm.html'), name = 'password_reset_confirm'), #<> are parameters we saw that we needed from debug screen
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'users/password_reset_comlete.html'), name = 'password_reset_complete'),
    path('users/', user_views.UserListView.as_view(template_name = 'users/user_list.html'), name = 'user-list'),
    
    path('', include('blog.urls')), #it chops off blog and checks if anything else is remaining, and tries to match that(which is a string) path on url patterns of urls.py of blog folder
    path('gallery/', include('gallery.urls')),
]

#to serve media files during development, This configuration will serve media files correctly when running the development server.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
