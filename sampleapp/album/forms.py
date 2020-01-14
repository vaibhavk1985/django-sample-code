"""Render all developers application forms."""
from multiupload.fields import MultiImageField
from django import forms
MAX_SIZE = 5 * 1024 * 1024
from .models import Album


class AlbumForm(forms.ModelForm):

    original_img = forms.ImageField()

    class Meta:
        model = Album
        fields = ('original_img', )
