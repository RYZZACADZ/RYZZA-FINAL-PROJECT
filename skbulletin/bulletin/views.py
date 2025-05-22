from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView

from .models import Announcement, Event, EmergencyAlert, Feedback
from .forms import AnnouncementForm, EventForm, EmergencyAlertForm, FeedbackForm

# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'bulletin/login.html'

    def get_success_url(self):
        return '/admin-dashboard/' if self.request.user.is_staff else '/'

# Public Views
def home(request):
    recent_announcements = Announcement.objects.order_by('-date_posted')[:3]
    return render(request, 'bulletin/home.html', {'recent_announcements': recent_announcements})

def announcements(request):
    posts = Announcement.objects.order_by('-date_posted')
    return render(request, 'bulletin/announcements.html', {'posts': posts})

def announcement_detail(request, pk):
    post = get_object_or_404(Announcement, pk=pk)
    return render(request, 'bulletin/announcement_detail.html', {'post': post})

def events(request):
    events = Event.objects.order_by('date', '-date_posted')
    return render(request, 'bulletin/events.html', {'events': events})

def alerts(request):
    alerts = EmergencyAlert.objects.order_by('-date_created')
    return render(request, 'bulletin/emergency_alerts.html', {'alerts': alerts})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            Feedback.objects.create(name=name, email=email, message=message)
            messages.success(request, "Thank you for submitting your message!")
            return redirect('contact')
        else:
            messages.error(request, "Please fill in all required fields.")
    return render(request, 'bulletin/contact.html')

def feedback(request):
    if request.method == 'POST':
        msg = request.POST.get('message')
        Feedback.objects.create(message=msg)
        return redirect('feedback')

    feedbacks = Feedback.objects.all() if request.user.is_staff else None
    return render(request, 'bulletin/feedback.html', {'feedbacks': feedbacks})

# Admin check
def is_admin(user):
    return user.is_authenticated and user.is_staff

# Admin Dashboard
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    announcement_form = AnnouncementForm()
    event_form = EventForm()
    alert_form = EmergencyAlertForm()

    if request.method == 'POST':
        if 'submit_announcement' in request.POST:
            announcement_form = AnnouncementForm(request.POST, request.FILES)
            if announcement_form.is_valid():
                announcement_form.save()
        elif 'submit_event' in request.POST:
            event_form = EventForm(request.POST, request.FILES)
            if event_form.is_valid():
                event_form.save()
        elif 'submit_alert' in request.POST:
            alert_form = EmergencyAlertForm(request.POST, request.FILES)
            if alert_form.is_valid():
                alert_form.save()

    context = {
        'announcement_form': announcement_form,
        'event_form': event_form,
        'alert_form': alert_form,
        'announcement_count': Announcement.objects.count(),
        'event_count': Event.objects.count(),
        'alert_count': EmergencyAlert.objects.count(),
        'feedback_count': Feedback.objects.count(),
    }

    return render(request, 'bulletin/admin_dashboard.html', context)


# API Views
def api_announcements(request):
    data = list(Announcement.objects.values())
    return JsonResponse(data, safe=False)

def api_events(request):
    data = list(Event.objects.values())
    return JsonResponse(data, safe=False)

def api_alerts(request):
    data = list(EmergencyAlert.objects.values())
    return JsonResponse(data, safe=False)

def api_feedback(request):
    data = list(Feedback.objects.values())
    return JsonResponse(data, safe=False)

# Optional Separate View to Create Announcement (if needed)
@user_passes_test(lambda u: u.is_staff)
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('announcements')
    else:
        form = AnnouncementForm()
    return render(request, 'bulletin/create_announcement.html', {'form': form})

#edit, delete
@login_required
def edit_announcement(request, id):
    if not request.user.is_staff:
        return redirect('home')
    announcement = get_object_or_404(Announcement, id=id)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcements')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'bulletin/edit_announcement.html', {'form': form})

@login_required
def delete_announcement(request, id):
    if not request.user.is_staff:
        return redirect('home')
    announcement = get_object_or_404(Announcement, id=id)
    announcement.delete()
    return redirect('announcements')

@login_required
def edit_event(request, id):
    if not request.user.is_staff:
        return redirect('home')
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events')
    else:
        form = EventForm(instance=event)
    return render(request, 'bulletin/edit_event.html', {'form': form})

@login_required
def delete_event(request, id):
    if not request.user.is_staff:
        return redirect('home')
    event = get_object_or_404(Event, id=id)
    event.delete()
    return redirect('events')

@login_required
def edit_alert(request, id):
    if not request.user.is_staff:
        return redirect('home')
    alert = get_object_or_404(EmergencyAlert, id=id)
    if request.method == 'POST':
        form = EmergencyAlertForm(request.POST, request.FILES, instance=alert)
        if form.is_valid():
            form.save()
            return redirect('alerts')  # Make sure you have this URL/view set up
    else:
        form = EmergencyAlertForm(instance=alert)
    return render(request, 'bulletin/edit_alert.html', {'form': form})


@login_required
def delete_alert(request, id):
    if not request.user.is_staff:
        return redirect('home')
    alert = get_object_or_404(EmergencyAlert, id=id)
    alert.delete()
    return redirect('alerts')

@login_required
def edit_feedback(request, id):
    if not request.user.is_staff:
        return redirect('home')
    feedback = get_object_or_404(Feedback, id=id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect('feedback')  # Make sure you have this URL/view set up
    else:
        form = FeedbackForm(instance=feedback)
    return render(request, 'bulletin/edit_feedback.html', {'form': form})

@login_required
def delete_feedback(request, id):
    if not request.user.is_staff:
        return redirect('home')
    feedback = get_object_or_404(Feedback, id=id)
    feedback.delete()
    return redirect('feedback')

def handler404(request, exception):
    return render(request, 'bulletin/404.html', status=404)

def handler500(request):
    return render(request, 'bulletin/500.html', status=500) 