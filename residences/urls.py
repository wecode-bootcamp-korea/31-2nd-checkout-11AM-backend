from django.urls import path

from .views import ResidenceDetailView, RoomDetailView

urlpatterns = [
    path('/<str:residence_name>', ResidenceDetailView.as_view()),
    path('/<str:residence_name>/room', RoomDetailView.as_view())
]
