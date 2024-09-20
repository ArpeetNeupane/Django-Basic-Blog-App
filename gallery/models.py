from django.db import models
from PIL import Image

class ImageUpload(models.Model):
    title = models.CharField(max_length=20)
    image = models.ImageField(default='default_gallery.jpeg', upload_to='gallery_pics')

    def __str__(self):
        return self.title

    #overriding save method
    #reszing image
    def save(self, *args, **kwargs):
        #this method runs after our model is saved
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 800 or img.width >1200:
            output_size = (800, 1200)
            img.resize(output_size)
            img.save(self.image.path)
