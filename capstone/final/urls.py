from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("<int:year>/<int:month>/<int:day>", views.day, name="day"),
    path("reserve", views.reserve, name="reserve"),
    path("user/<str:user>", views.user_rvs, name="user_rvs"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("wait", views.wait, name="wait"),
]