from django.urls import path
from . import api_views

urlpatterns = [
    path('announcements/', api_views.AnnouncementList.as_view(), name='api-announcements'),
    path('events/', api_views.EventList.as_view(), name='api-events'),
]
