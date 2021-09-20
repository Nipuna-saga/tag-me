from . import views
from django.urls import path

urlpatterns = [
    path("", views.TagView.as_view(), name="tag"),
]
