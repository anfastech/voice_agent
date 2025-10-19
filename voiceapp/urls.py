# urls.py (in your app directory)
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'voiceapp'

urlpatterns = [
    path('', views.index_view, name='index'),
    # path('success/', views.success, name='success'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)