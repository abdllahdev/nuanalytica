from django.urls import path
from . import views

app_name = "analytica_app"

urlpatterns = [
    path(
        "",
        view=views.AppView.as_view(),
        name='app_view'
    ),
]
