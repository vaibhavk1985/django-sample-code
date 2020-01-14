from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from api.serializers import AlbumCreateSerializer
from album.models import Album
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from api.helpers import modify_input_for_multiple_files
from rest_framework.views import APIView


class AlbumCreate(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AlbumCreateSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        all_albums = Album.objects.all()
        serializer = AlbumCreateSerializer(all_albums, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        album_data = request.data
        images = dict((album_data).lists())['original_img']
        flag = 1
        arr = []
        for img_name in images:
            modified_data = modify_input_for_multiple_files(img_name)
            file_serializer = AlbumCreateSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)