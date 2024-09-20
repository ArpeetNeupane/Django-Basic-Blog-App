from django.db.models.signals import post_save
#this is a signal that gets fired after an object is saved
#in this case, we want to get a posts save signal when a user is created, hence user needs to be imported as well
from django.contrib.auth.models import User
#user model is the sender in this case, since it is what sends the signal
from django.dispatch import receiver
#a receiver is a function that receives this function and does some task
from .models import Profile

@receiver(post_save, sender=User) #means when a user is saved, send post_save signal and that signal is going to be 
#received by the receiver which is create_profile function
def create_profile(sender, instance, created, **kwargs): 
    if created: #if that user was created, create profile
        Profile.objects.create(user = instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs): #accepts any additional keyword argument onto the end of the function
    instance.profile.save() #instance means user
    #saves any changes made to the Profile object associated with the User.