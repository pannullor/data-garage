from django.urls import path

from .views import RaceView

app_name = 'analytics'
urlpatterns = [
    path('race/<str:name>/', RaceView.as_view(), name='race-view'),
]