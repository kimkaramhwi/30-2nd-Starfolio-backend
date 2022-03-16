from django.urls import path, include

urlpatterns = [
    path('planets', include('planets.urls')),
]
