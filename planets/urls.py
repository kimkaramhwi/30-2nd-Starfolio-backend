from django.urls import path

from planets.views import PlanetListView

urlpatterns = [
    path('', PlanetListView.as_view()),
]