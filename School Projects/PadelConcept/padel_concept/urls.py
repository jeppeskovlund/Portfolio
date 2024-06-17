"""
Denne fil indeholder URL-konfigurationen for hele Padel Concept-projektet.

urls.py på projektet bruges til at dirigere URL-forespørgsler til de korrekte applikationer.
Den inkluderer URL-mønstre fra applikationer og definerer stier til admin-panelet.

Indeholder følgende URL-mønstre:
1. "admin/" - Dirigerer til admin-panelet.
2. "" - Inkluderer URL-mønstre fra tournament-applikationen.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tournament.urls")),
]
