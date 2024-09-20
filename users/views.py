from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import User

def register(request):
    #in-built registration form(just need to import it), forms are classes which will be converted to html
    if request.method == 'POST':
        form_instance = UserRegisterForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            username = form_instance.cleaned_data.get('username') #getting username from the reg form, cleaned_data is a dictionary
            messages.success(request, f"Your account has been created with Username { username }. You are able to login now!")
            #this is a flash message. flash message is an easy way for us to send one-time alert to a template that will only be displayed once and ill dissapear on the next request.
            return redirect('login')
    else:
        form_instance = UserRegisterForm()
    return render(request, 'users/register.html', {'form' : form_instance}) 

#this is the way to logout in newer django version
def logout_view(request):
    logout(request)
    return render(request, 'users/logout.html')

@login_required #decorators add functionality to existing function
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user) #if left empty(argument), current user's data cant be seen on profile
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile) ####didn't understand request.POST####
    else:
        u_form = UserUpdateForm(instance=request.user) #if left empty(argument), current user's data cant be seen on profile
        p_form = ProfileUpdateForm(instance=request.user.profile)

    #if new datas are valid, update form
    if u_form.is_valid() and p_form.is_valid(): 
        if u_form.changed_data or p_form.changed_data:
            u_form.save()
            p_form.save()
            messages.success(request, f"Your profile has been updated!")
            return redirect('profile') #need to redirect and not let it fall to render, because POST GET redirect pattern
        else:
            messages.info(request, "No changes were made to your profile.")
            return redirect('profile')

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request, 'users/profile.html', context)

#django keeps track of where the user wanted to go, so if the user tries to go to profile without login, 
#they will be redirected to login page and the url has next = /profile/ which means that after the user logs in
#they are sent to the page they were trying to go to

class UserListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'users'

