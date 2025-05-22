from django.contrib import admin
from .models import Announcement, Event, EmergencyAlert, Feedback, Contact

# Register your models here
admin.site.register(Announcement)
admin.site.register(Event)
admin.site.register(EmergencyAlert)
admin.site.register(Feedback)
admin.site.register(Contact)
