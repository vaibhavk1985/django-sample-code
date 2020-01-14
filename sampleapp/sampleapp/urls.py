"""sampleapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path
from django.conf.urls import include
from users.views import UserSignup, HomeView, activate
from django.views.generic import TemplateView
from album.views import AlbumUploadView
from django.conf import settings
from django.conf.urls.static import static
from api.views import AlbumCreate


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('django.contrib.auth.urls')),
    path("user/register/", UserSignup.as_view(), name="register"),
    path('', HomeView.as_view(), name="home"),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            activate, name='activate'),
    re_path(r'^api-auth/', include('rest_framework.urls')),
    re_path(r'^rest-auth/', include('rest_auth.urls')),
    re_path(r'^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(template_name='registration/empty.html'),name='account_confirm_email'),
    re_path(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    path("album/create/", AlbumUploadView.as_view(), name="album_create"),
    re_path(r'^api/albums', AlbumCreate.as_view(), name='create_album'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)