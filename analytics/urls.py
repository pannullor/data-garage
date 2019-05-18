from django.urls import path
from .views import AnalyticsView

app_name = 'analytics'
urlpatterns = [
    path('<int:year>/', AnalyticsView.as_view(), name='analytics'),
]