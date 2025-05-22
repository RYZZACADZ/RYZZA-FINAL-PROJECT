from rest_framework import generics # type: ignore
from .models import Announcement, Event
from .serializers import AnnouncementSerializer, EventSerializer

class AnnouncementList(generics.ListAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

class EventList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
