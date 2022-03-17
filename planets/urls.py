from django.urls import path

from planets.views import PlanetListView, PlanetDetailView

urlpatterns = [
    path('', PlanetListView.as_view()),
    path('/planet/<int:planet_id>/accomodation/<int:accomodation_id>', PlanetDetailView.as_view())
]