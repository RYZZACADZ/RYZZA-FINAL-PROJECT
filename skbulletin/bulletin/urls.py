from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('announcements/', views.announcements, name='announcements'),
    path('announcements/create/', views.create_announcement, name='create_announcement'),  # ✅ New line
    path('events/', views.events, name='events'),
    path('alerts/', views.alerts, name='alerts'),
    path('contact/', views.contact, name='contact-us'),
    path('contact/', views.contact, name='contact'),
    path('feedback/', views.feedback, name='feedback'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('announcements/<int:pk>/', views.announcement_detail, name='announcement-detail'),

#edit/delete
    path('announcements/edit/<int:id>/', views.edit_announcement, name='edit_announcement'),
    path('announcements/delete/<int:id>/', views.delete_announcement, name='delete_announcement'),
    path('events/edit/<int:id>/', views.edit_event, name='edit_event'),
    path('events/delete/<int:id>/', views.delete_event, name='delete_event'),
    path('alerts/edit/<int:id>/', views.edit_alert, name='edit_alert'),
    path('alerts/delete/<int:id>/', views.delete_alert, name='delete_alert'),
    path('feedback/<int:pk>/edit/', views.edit_feedback, name='edit_feedback'),
path('feedback/<int:pk>/delete/', views.delete_feedback, name='delete_feedback'),


    #  NEW API ENDPOINTS
    path('api/announcements/', views.api_announcements, name='api_announcements'),
    path('api/events/', views.api_events, name='api_events'),
    path('api/alerts/', views.api_alerts, name='api_alerts'),
    path('api/feedback/', views.api_feedback, name='api_feedback'),
]


