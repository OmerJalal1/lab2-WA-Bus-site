from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("route/<int:route_id>", views.route, name="route"),
    path("station/<int:station_id>", views.station, name="station"),
    path("my-routes", views.my_routes, name="my_routes"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("book/<int:route_id>", views.book, name="book"),
    path("unbook/<int:route_id>", views.unbook, name="unbook"),
]
