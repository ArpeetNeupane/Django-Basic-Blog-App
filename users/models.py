from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #we want a 1-1 relation with User so we passed that as argument
    #if user is deleted, profile is deleted(one way, not the other way round)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    #profile_pics is the directory which is created (where pfps are stored)
    birthday = models.DateField(default=datetime.date.today)

    #we're making a dunder str method so that when we print profile, we dont want it to say profile object(in admin) but
    #be more descriptive the way we want
    def __str__(self):
        #self is the instance
        return f"{self.user.username}'s Profile"
        #it will return eg;TestUser01 Profile when profile is printed

    #overriding save method
    #reszing image
    def save(self, *args, **kwargs):
        #this method runs after our model is saved
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width >300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
