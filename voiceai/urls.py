
"""
urls.py: The URL dispatcher, encoded within urls.py: maps URLs to views. This file determines which view is displayed when a specific URL is accessed. It's like a roadmap that navigates users through the intricacies of your application's pages.
"""

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('voiceapp.urls')),
]
