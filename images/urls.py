from . import views
from django.urls import path

urlpatterns = [
    path("", views.ImageView.as_view()),
]
