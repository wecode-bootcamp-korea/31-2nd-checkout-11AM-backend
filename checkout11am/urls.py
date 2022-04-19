from django.urls import path, include


urlpatterns = [
    path('users', include('users.urls')),
    path('residences', include('residences.urls'))
]
