from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ImageUpload
from .forms import PhotoUpload

#Gallery view to display the images
@login_required()
def gallery(request):
    photos = ImageUpload.objects.all().distinct()
    return render(request, 'gallery/photo_library.html', {'photos': photos})

#upload view
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoUpload(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery-home')
    else:
        form = PhotoUpload()
    return render(request, 'gallery/photo_upload.html', {'form': form})