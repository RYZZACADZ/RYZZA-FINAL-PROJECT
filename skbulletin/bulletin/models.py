from django.db import models
from django.utils import timezone


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='announcement_images/', blank=True, null=True)  
    date_posted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
class Event(models.Model):
    EVENT_STATUS = (
        ('PENDING', 'Pending'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=EVENT_STATUS, default='PENDING')
    date_posted = models.DateTimeField(default=timezone.now)
    date = models.DateField()

    def __str__(self):
        return self.name

class EmergencyAlert(models.Model):
    description = models.TextField()
    message = models.TextField()
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='alert_images/', blank=True, null=True)

    def __str__(self):
        return f"EmergencyAlert at {self.date_created}"

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.submitted_at}"

class Contact(models.Model):
    official_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.official_name
