"""
Denne fil indeholder URL-konfigurationen for Tournament-applikationen.

urls.py bruges til at definere URL-mønstre, der matcher URL-forespørgsler med de tilsvarende views.
Hver URL-sti er forbundet med en specifik view-funktion eller klasse, som håndterer HTTP-forespørgsler og returnerer svar.

Indeholder følgende URL-mønstre:
1. "/" - Viser en liste over turneringer.
2. "/tournament/<int:pk>/" - Viser detaljer for en specifik turnering.
3. "/tournament/<int:pk>/schedule/" - Viser tidsplanen for en specifik turnering.
4. "/tournament/<int:pk>/signup/" - Håndterer tilmelding til en specifik turnering.
5. "/match/<int:match_id>/result-form/" - Viser formularen til indrapportering af kampresultater.
6. "/tournament/<int:pk>/signups/" - Viser tilmeldingerne til en specifik turnering.
"""

from django.urls import path

from .views import (
    TournamentDetailView,
    TournamentListView,
    TournamentScheduleView,
    get_tournament_signups,
    match_result_form,
    tournament_signup,
)

urlpatterns = [
    path("", TournamentListView.as_view(), name="tournament-list"),
    path(
        "tournament/<int:pk>/", TournamentDetailView.as_view(), name="tournament-detail"
    ),
    path(
        "tournament/<int:pk>/schedule/",
        TournamentScheduleView.as_view(),
        name="tournament-schedule",
    ),
    path("tournament/<int:pk>/signup/", tournament_signup, name="tournament-signup"),
    path(
        "match/<int:match_id>/result-form/", match_result_form, name="match-result-form"
    ),
    path(
        "tournament/<int:pk>/signups/",
        get_tournament_signups,
        name="tournament-signups",
    ),
]
