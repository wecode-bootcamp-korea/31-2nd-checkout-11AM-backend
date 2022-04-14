from django.urls import path

from .views import ResidenceListView, RoomDetailView, ResidenceDetailView

urlpatterns = [
    path('', ResidenceListView.as_view()),
     path('/<int:residence_id>', ResidenceDetailView.as_view()),
    path('/<int:residence_id>/room/<int:room_id>', RoomDetailView.as_view())
]
