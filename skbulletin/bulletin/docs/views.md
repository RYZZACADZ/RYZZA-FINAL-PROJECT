# Event Views Documentation

## Overview
The views handle the display and management of events in the SK Bulletin system. They include both public views for residents and administrative views for staff members.

## Public Views

### `events(request)`
Displays all events to the public.

```python
def events(request):
    events = Event.objects.order_by('date', '-date_posted')
    return render(request, 'bulletin/events.html', {'events': events})
```

- **Purpose**: Shows all events with their status
- **Sorting**: Events are sorted by date (ascending) and post date (descending)
- **Template**: Uses `events.html`
- **Access**: Public (no login required)
- **Features**:
  - Displays event status badges
  - Shows event details (name, description, location, date)
  - Responsive design for all devices

## Administrative Views

### `admin_dashboard(request)`
Administrative interface for managing events.

```python
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # View implementation
```

- **Access**: Staff only (requires login)
- **Decorators**: 
  - `@login_required`
  - `@user_passes_test(is_admin)`
- **Features**:
  - Create new events
  - View event statistics
  - Access to all event management features

### `edit_event(request, id)`
Allows staff to edit existing events.

```python
@login_required
def edit_event(request, id):
    if not request.user.is_staff:
        return redirect('home')
    # View implementation
```

- **Access**: Staff only
- **Parameters**: 
  - `id`: Event ID to edit
- **Features**:
  - Update event details
  - Change event status
  - Modify dates and information

### `delete_event(request, id)`
Allows staff to delete events.

```python
@login_required
def delete_event(request, id):
    if not request.user.is_staff:
        return redirect('home')
    # View implementation
```

- **Access**: Staff only
- **Parameters**: 
  - `id`: Event ID to delete
- **Security**: Confirms user is staff before deletion

## Template Details

### events.html
The main template for displaying events.

#### Key Features:
1. Status Badge Display
   ```html
   <span class="badge {% if event.status == 'PENDING' %}bg-warning
                      {% elif event.status == 'ONGOING' %}bg-success
                      {% elif event.status == 'COMPLETED' %}bg-secondary
                      {% else %}bg-danger{% endif %} text-white">
       {{ event.get_status_display }}
   </span>
   ```

2. Event Information Layout
   - Name and status at the top
   - Description with "Read more" option
   - Location and date information
   - Category badge if available

3. Administrative Controls
   - Edit and delete buttons for staff
   - Confirmation dialog for deletion

## Form Integration

### EventForm
Handles event creation and editing.

```python
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'image', 
                 'category', 'status', 'date']
```

- **Fields**: All essential event information
- **Widgets**: Enhanced with Bootstrap styling
- **Validation**: Built-in Django form validation

## API Integration

### `api_events(request)`
JSON API endpoint for events.

```python
def api_events(request):
    data = list(Event.objects.values())
    return JsonResponse(data, safe=False)
```

- **Purpose**: Provides event data in JSON format
- **Usage**: External integrations and AJAX requests 