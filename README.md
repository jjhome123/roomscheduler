
# CS50w Final Project - Classroom Scheduler

## Introduction

Hello! Thank you very much for taking the time to read about my CS50w final project.
For my capstone, I decided to make an application that allows approved users to book school classrooms.

After logging into the app with an approved account, users can navigate to a particular day, choose a specific room, and set a time period that they would like to reserve it for.

Assuming that the reservation does not coincide with another, the user will successfully make the reservation and it will be reflected on the schedule for that day.
***
## Distinctiveness & *Complexity*

This project satisfies the distinctiveness requirement as it is neither a search engine, e-mail app, social networking site nor a Wikipedia derivative.
Similar to the Mail and Network projects, a user account is necessary to navigate the application but user registration must be approved by a site administrator. Account approval is given through the Django admin interface, where the site administrator would manually check pending accounts' "is_active" status to "True."

In terms of complexity, I believe my application satisfies this requirement because of three overarching points: interaction with daily timetables, reservation validation, and user pages.

### Daily Timetables

#### Timeslot Status

When viewing the timetable for a particular day, a user will see any of the three following statuses for a timeslot: "Reserved," "Available," or "Passed."
- "Reserved" is denoted by the salmon pink background given to a timeslot with the reserver's username in that timeslot.
- "Available" is denoted by a white, transparent background and an "O".  These cells are clickable and can transfer timeslot information to the form at the top of the page. 
    - **Note:** Open timeslots are only interactive if a user is logged in - anonymous users cannot select start and end times for a reservation.
- "Passed" is denoted by a grey background and either a "-" or a reserver's username.
How a cell shows a particular status will depend on the current time and whether a reservation is present within that timeslot.

#### Viewing Different Timetables

In order to view the timetable for another day, a user can select a day at the top of a timetable to load the reservations for that day. In the case of timeslots that have already happened, they will be automatically hidden from the user's view.

#### Viewing Previous Timeslots

For timetables for past days, users can check the "Show Previous Timeslots" to view all previous timeslots for that day. Using a bit of JavaScript, each cell with a "passed" class is set to `display: none;`.

#### Making a Reservation from the Timetable View

If a user is viewing a timetable for the current day or for a day in the future, they have the ability to click "Available" timeslots to make a reservation. Once a user clicks the first available timeslot, the cell's background will become blue. At the same time, the start time and room will be inputted into the reservation form above the timetable. Then, once a user clicks another timeslot, this cell's background will become red to denote the end time of the reservation. Like the first cell, the end time will be inputted into the reservation form as well.

### Reservation Validation

#### Selecting Timeslots (Front-End Validation)

When viewing a timetable, "Available" slots can be selected to make a room reservation. Clicking on cells will turn their backgrounds blue to indicate the start time and red to indicate the end time. If a user clicks on an available start time to turn it blue and then clicks on an earlier time for the end time, the new start time will become that earlier time and this will be reflected in the form above the timetable.

**Note:** This functionality is only for available timeslots. Cells that have pre-existing reservations or are for times that have already happened cannot be selected.

Additionally, the button for the reservation form is by default disabled and only submittable once a valid start and end time are inputted into the reservation form.

#### Back-End Validation
Reservations will not be made in the following cases:
- The reservation is for a day that has already happened
- The reservation's end time is earlier than the start time
- The reservation's start/end time coincides with a previously made reservation for a room
- The reservation starts before and ends after a pre-existing reservation
- The start time and end time for a reservation are for different rooms

### User Pages

From the timetable, users can click on timeslots with usernames in them to be directed to a user's page. Each user's page shows upcoming and past reservations associated with the user.

At the top of the navigation bar, a user can click "My Reservations" in order to view their own user page. At this page, a user can delete upcoming reservations they have made.

**Note:** Deleting upcoming reservations is only possible on a user's My Reservations page. They are not able to delete other users' reservations.
***
## Project Contents

### Python Files
#### `admin.py`

This file registers three models to the admin interface: `Reservation`, `Room`, and `User`.

#### `models.py`

- `User`: From Django's default User model and AbstractUser subclass.  
- `Room`: "name" `CharField` for room names
- `Reservation`:
    - `User` as `ForeignKey`
    - `date` as `DateField`
    - `Room` as `ForeignKey`
    - `Start` as `DateTimeField`
    - `End` as `DateTimeField`

#### `views.py`
- `index`
    - GET: Displays timetable for current day
    - POST: Either navigates to different timetable day OR makes reservation
- `day` - Same as index, but datetime reflected in URL and displays timetable for particular day
- `reserve`
    - GET: Displays a reservation form
    - POST: Creates reservation based on form input
- `user_rvs`
    - GET: Displays a user's upcoming/past reservations
    - POST: Deletes a user reservation
- `login_view`
    - GET: Displays login form
    - POST: Authenticates credentials and logs user in
- `logout_view` - Logs user out.
- `register`
    - GET: Displays user registration form
    - POST: Adds new inactive user to user base.
- `wait` - After registration, directs new user to a registration pending page

#### `urls.py`
- Eight paths: One for each view in `views.py`

### Static Files

#### `final.js`
Contains all of the JavaScript responsible for timeslot color changes, making reservations at the timetable view, and the enabling/disabling of buttons.

#### `styles.css`
Contains minor style adjustments outside of Bootstrap styling.
***
## How to Run this Application

Running the command `python manage.py runserver` will allow you to run the application on a development server.