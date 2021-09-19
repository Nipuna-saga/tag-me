from . import views
from django.urls import path

urlpatterns = [
    path("<str:image_id>/tag/", views.tag_image),
    path("", views.ImageView.as_view()),

]
