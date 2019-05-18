from django.urls import path
from . import views as AnalyticsViews

app_name = 'analytics'
urlpatterns = [
    path('<int:year>/', AnalyticsViews.AnalyticsBaseView.as_view(), name='analytics'),
    path('trends/<int:race_id>/', AnalyticsViews.AnalyticsTrendsView.as_view(), name='trends'),
]