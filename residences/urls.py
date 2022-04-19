from django.urls import path

from .views import ResidenceListView

urlpatterns = [
    path('', ResidenceListView.as_view())
]