import datetime, json
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

# Create your views here.

def index(request):
    if request.method == 'POST':
        date = request.POST['form_date'].split('-')
        return day(request, year=int(date[0]),month=int(date[1]),day=int(date[2]))
    # Get all rooms
    rooms = Room.objects.all()
    today = datetime.datetime.today()
    # Create array of datetime objects to be used as timeslot indicators
    timeslots = []
    time = datetime.datetime(today.year, today.month, today.day, 7, 30, 0, 0)
    i = datetime.timedelta(minutes=5)
    while time != datetime.datetime(today.year, today.month, today.day, 17, 5, 0, 0):
        timeslots.append(time)
        time += i
    # Create array of reservations
    reservation_list = []
    for slot in timeslots:
        row = {}
        row["time"] = slot
        for room in rooms:       
            reservations = room.reservations.filter(date=today)
            if reservations:
                for reservation in reservations:
                    if slot >= reservation.start and slot <= reservation.end:
                        if slot < today:
                            row[reservation.room.name] = f"({reservation.user.username})"
                        else:
                            row[reservation.room.name] = reservation.user.username
                        break
                    else:
                        if slot < today:
                            row[reservation.room.name] = "-"                        
                        else:
                            row[reservation.room.name] = "O"
            else:
                if slot < today:
                    row[room] = "-"
                else:
                    row[room] = "O"
        reservation_list.append(row)
    #GET View
    return render(request, "final/index.html", {
        "user": request.user,
        "datetime": today,
        "rooms": rooms,
        "reservations": reservation_list,
    })


def day(request,year,month,day):
    if request.method == 'POST':
        date = request.POST['form_date'].split('-')
        dtm = datetime.datetime(year=int(date[0]),month=int(date[1]),day=int(date[2]))
    else:
        dtm = datetime.datetime(year=year,month=month,day=day)
    rooms = Room.objects.all()
    today = datetime.datetime.today()
    # Create array of datetime objects to be used as timeslot indicators
    timeslots = []
    time = datetime.datetime(dtm.year, dtm.month, dtm.day, 7, 30, 0, 0)
    i = datetime.timedelta(minutes=5)
    while time != datetime.datetime(dtm.year, dtm.month, dtm.day, 17, 5, 0, 0):
        timeslots.append(time)
        time += i
    # Create array of reservations
    reservation_list = []
    for slot in timeslots:
        row = {}
        row["time"] = slot
        for room in rooms:       
            reservations = room.reservations.filter(date=dtm)
            if reservations:        
                for reservation in reservations:
                    if slot >= reservation.start and slot <= reservation.end:

                        if slot < today:
                            row[reservation.room.name] = f"({reservation.user.username})"
                        else:
                            row[reservation.room.name] = reservation.user.username
                        break
                    else:
                        if slot < today:
                            row[reservation.room.name] = "-"                        
                        else:
                            row[reservation.room.name] = "O"
            else:
                if slot < today:
                    row[room] = "-"
                else:
                    row[room] = "O"
        reservation_list.append(row)
    #GET View
    return render(request, "final/index.html", {
        "user": request.user,
        "datetime_dayview": today,
        "datetime": dtm,
        "rooms": rooms,
        "reservations": reservation_list,
    })


@login_required
def reserve(request):
    rooms = Room.objects.all()
    timeslots = []
    time = datetime.datetime(1000, 1, 1, 7, 30, 0, 0)
    i = datetime.timedelta(minutes=5)
    while time != datetime.datetime(1000, 1, 1, 17, 5, 0, 0):
        timeslots.append(time)
        time += i
    if request.method == "POST":
        date = datetime.datetime.strptime(request.POST.get("date"), "%Y-%m-%d")
        # Convert POSTed data into a timedate object to compare
        if 'a.m.' in request.POST.get('start'):
            s = request.POST.get('start').replace('a.m.','AM')
            try:
                start = datetime.datetime.strptime(s, "%b. %d, %Y, %I %p")
            except ValueError:
                try:
                    start = datetime.datetime.strptime(s, "%b. %d, %Y, %I:%M %p")
                except ValueError:
                    try:
                        start = datetime.datetime.strptime(s, "%B %d, %Y, %I %p")
                    except ValueError:
                        start = datetime.datetime.strptime(s, "%B %d, %Y, %I:%M %p")
        elif 'p.m.' in request.POST.get('start'):
            s = request.POST.get('start').replace('p.m.','PM')
            try:
                start = datetime.datetime.strptime(s, "%b. %d, %Y, %I %p")
            except ValueError:
                try:
                    start = datetime.datetime.strptime(s, "%b. %d, %Y, %I:%M %p")
                except ValueError:
                    try:
                        start = datetime.datetime.strptime(s, "%B %d, %Y, %I %p")
                    except ValueError:
                        start = datetime.datetime.strptime(s, "%B %d, %Y, %I:%M %p")
        if 'a.m.' in request.POST.get('end'):
            s = request.POST.get('end').replace('a.m.','AM')
            try:
                end = datetime.datetime.strptime(s, "%b. %d, %Y, %I %p")
            except ValueError:
                try:
                    end = datetime.datetime.strptime(s, "%b. %d, %Y, %I:%M %p")
                except ValueError:
                    try:
                        end = datetime.datetime.strptime(s, "%B %d, %Y, %I %p")
                    except ValueError:
                        end = datetime.datetime.strptime(s, "%B %d, %Y, %I:%M %p")
        elif 'p.m.' in request.POST.get('end'):
            s = request.POST.get('end').replace('p.m.','PM')
            try:
                end = datetime.datetime.strptime(s, "%b. %d, %Y, %I %p")
            except ValueError:
                try:
                    end = datetime.datetime.strptime(s, "%b. %d, %Y, %I:%M %p")
                except ValueError:
                    try:
                        end = datetime.datetime.strptime(s, "%B %d, %Y, %I %p")
                    except ValueError:
                        end = datetime.datetime.strptime(s, "%B %d, %Y, %I:%M %p")
        else:
            hour, min = request.POST.get("start").split(':')
            start = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=int(hour), minute=int(min))
            hour, min = request.POST.get("end").split(':')
            end = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=int(hour), minute=int(min))
        start = start.replace(year=date.year,month=date.month,day=date.day)
        end = end.replace(year=date.year,month=date.month,day=date.day)
        room = Room.objects.get(name=request.POST.get("room"))
        
        # Validate POSTed data
        today = datetime.datetime.today()
        r = Reservation.objects.filter(date=date, room=room)
        for rv in r:
            if (start >= rv.start and start <= rv.end) or (end >= rv.start and end <= rv.end) or (start <= rv.start and end >= rv.end):
                return render(request, 'final/reserve.html', {
                    "rooms": rooms,
                    "timeslots": timeslots,
                    "error": "Error: Reservation coincides with another"
                }) 
        if start < today:
            return render(request, 'final/reserve.html', {
                "rooms": rooms,
                "timeslots": timeslots,
                "error": "Error: Cannot make a reservation for a date that has already happened"
            })
        if start > end:
            return render(request, 'final/reserve.html', {
                "rooms": rooms,
                "timeslots": timeslots,
                "error": "Error: Start time cannot be later than end time"
            })
        elif start == end:
            return render(request, 'final/reserve.html', {
                "rooms": rooms,
                "timeslots": timeslots,
                "error": "Error: Start and end times cannot be the same"
            })
        else:
            Reservation.objects.create(user=request.user, date=date, room=room, start=start, end=end)
            return HttpResponseRedirect(f'/{date.year}/{date.month}/{date.day}')
        
    # GET request
    return render(request, 'final/reserve.html', {
        "rooms": rooms,
        "timeslots": timeslots,
    })


def user_rvs(request, user):
    if request.method == 'POST':
        data = json.loads(request.body)
        room = data["room"]
        year,month,day = data["date"].split('-')
        date = datetime.date(year=int(year),month=int(month),day=int(day))
        start_h, start_m = data["start"].split(':')
        start = datetime.datetime(year=date.year,month=date.month,day=date.day,hour=int(start_h),minute=int(start_m))
        end_h, end_m = data["end"].split(':')
        u = User.objects.get(username=request.user.username)
        print(u)
        end = datetime.datetime(year=date.year,month=date.month,day=date.day,hour=int(end_h),minute=int(end_m))
        r = Reservation.objects.get(user=u, date=date,room=Room.objects.get(name=room),start=start,end=end)
        r.delete()
    if request.user.username != user:
        reservations = Reservation.objects.filter(user=User.objects.get(username=user))
    else:
        reservations = Reservation.objects.filter(user=request.user)
    reservations_p = []
    reservations_u = []
    for reservation in reservations:
        rv = datetime.datetime(year=reservation.date.year,month=reservation.date.month,day=reservation.date.day,hour=reservation.start.hour,minute=reservation.start.minute)
        if rv >= datetime.datetime.now():
            reservations_u.append(reservation)
        else:
            reservations_p.append(reservation)
    return render(request, 'final/user_rvs.html', {
        'reserver': user,
        'reservations_p': reservations_p,
        'reservations_u': reservations_u
    })


def login_view(request):
    if request.method == "POST":

        # Sign-in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # If auth success
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        elif User.objects.get(username=username).is_active == False:
            return render(request, "final/login.html", {
                "message": "Account approval is still review. Please wait until your account has been approved."
            })
        else:
            return render(request, "final/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "final/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "final/register.html", {
                "message": "Passwords must match."
            })
        elif '' in [username,password,confirmation]:
            return render(request, "final/register.html", {
                "message": "All fields must be filled in."
            })

        try:
            user = User.objects.create_user(username=username, password=password, is_active=False)
            user.save()
        except IntegrityError:
            return render(request, "final/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("wait"))
    else:
        return render(request, "final/register.html")
    

def wait(request):
    return render(request, "final/wait.html")