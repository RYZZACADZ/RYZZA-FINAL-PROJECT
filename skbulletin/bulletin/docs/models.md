# Event Model Documentation

## Overview
The Event model represents events in the SK Bulletin system. It includes features for tracking event status, details, and related information.

## Model Fields

### Basic Information
- `name` (CharField, max_length=200)
  - The name/title of the event
  - Required field

- `description` (TextField)
  - Detailed description of the event
  - Can contain multiple paragraphs

- `location` (CharField, max_length=200)
  - Where the event will take place
  - Required field

### Status and Timing
- `status` (CharField, max_length=20)
  - Tracks the current state of the event
  - Choices:
    - `PENDING`: Event is scheduled but hasn't started
    - `ONGOING`: Event is currently happening
    - `COMPLETED`: Event has finished
    - `CANCELLED`: Event was cancelled
  - Default value: 'PENDING'

- `date` (DateField)
  - The date when the event will occur
  - Required field

- `date_posted` (DateTimeField)
  - When the event was posted
  - Automatically set to current time when created

### Additional Information
- `image` (ImageField)
  - Event poster or related image
  - Optional field
  - Stored in 'event_images/' directory
  - Supports blank and null values

- `category` (CharField, max_length=100)
  - Event category/type
  - Optional field
  - Can be left blank

## Usage Example

```python
# Creating a new event
event = Event.objects.create(
    name="Youth Leadership Summit",
    description="Annual leadership training for youth leaders",
    location="SK Hall",
    status="PENDING",
    date="2024-05-01"
)

# Updating event status
event.status = "ONGOING"
event.save()

# Querying events by status
ongoing_events = Event.objects.filter(status="ONGOING")
completed_events = Event.objects.filter(status="COMPLETED")
```

## Status Color Coding
The status is displayed with different colors in the UI:
- PENDING: Yellow badge
- ONGOING: Green badge
- COMPLETED: Gray badge
- CANCELLED: Red badge

## Important Notes
1. Events are automatically sorted by date in the view
2. Images are optional but recommended for better visual appeal
3. Status should be updated manually as the event progresses
4. Each status change is tracked and displayed to users 