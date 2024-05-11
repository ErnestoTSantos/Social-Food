from django.contrib import admin
from django.urls import path

from donations.apps.voluntary.views import VoluntaryView
from donations.apps.voluntary.views import ShelterView
from donations.apps.voluntary.views import VoluntaryAllocationView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/voluntary/", VoluntaryView.as_view()),
    path("api/v1/shelter/", ShelterView.as_view()),
    path("api/v1/voluntary-allocation/", VoluntaryAllocationView.as_view()),
]
