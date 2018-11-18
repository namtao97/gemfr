"""gemfr URL Configuration

The `urlpatterns` list routes URLs to   ews. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path

from webcam.views import webcam, face_recognition, human_detection, local

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webcam/', webcam),
    path('human_detection/', human_detection, name="human-detection"),
    path('face_recognition/', face_recognition, name="face-recognition"),
    path('local/', local, name='local')
]
