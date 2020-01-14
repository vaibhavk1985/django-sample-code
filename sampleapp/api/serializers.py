from rest_framework import serializers
from album.models import Album


class AlbumCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = ['original_img']