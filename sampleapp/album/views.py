from django.shortcuts import render

# Create your views here.

from django.views.generic.edit import FormView
from .forms import AlbumForm
from .models import Album


class AlbumUploadView(FormView):
    template_name = 'album/form.html'
    form_class = AlbumForm
    success_url = '/'

    def form_valid(self, form):
        for each in self.request.FILES.getlist('original_img'):
            Album.objects.create(original_img=each)
        return super(AlbumUploadView, self).form_valid(form)