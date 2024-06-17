"""
Denne fil indeholder views til Tournament-applikationen.

views.py bruges til at definere, hvordan forskellige HTTP-forespørgsler skal håndteres og hvilke templates der skal renderes.
Hver view-funktion eller -klasse er ansvarlig for at forberede data og returnere den korrekte HTML-svar.

Indeholder følgende views:
1. match_result_form - Håndterer indrapportering af kampresultater.
2. TournamentListView - Viser en liste over alle turneringer.
3. TournamentDetailView - Viser detaljer for en specifik turnering.
4. TournamentScheduleView - Viser tidsplanen for en specifik turnering.
5. tournament_signup - Håndterer tilmelding til en specifik turnering.
6. get_tournament_signups - Viser tilmeldingerne til en specifik turnering.
"""

from datetime import date

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET
from django.views.generic import DetailView, ListView

from .forms import MatchResultForm, SignupForm
from .models import Match, Team, Tournament


@staff_member_required
def match_result_form(request, match_id):
    """
    Håndterer indrapportering af kampresultater.
    Kræver, at brugeren er logget ind som medarbejder.
    """
    match = get_object_or_404(Match, id=match_id)
    if request.method == "POST":
        form = MatchResultForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect("tournament-schedule", pk=match.bracket.tournament.pk)
    else:
        form = MatchResultForm(instance=match)
    return render(
        request,
        "tournament/match_result_form.html",
        {"form": form, "match": match},
    )


class TournamentListView(ListView):
    """
    Viser en liste over alle turneringer.
    Bruger skabelonen 'index.html'.
    """

    model = Tournament
    template_name = "index.html"
    context_object_name = "tournaments"

    def get_queryset(self):
        return Tournament.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        context["upcoming_tournaments"] = Tournament.objects.filter(date__gte=today)
        context["finished_tournaments"] = Tournament.objects.filter(date__lt=today)
        return context


class TournamentDetailView(DetailView):
    """
    Viser detaljer for en specifik turnering.
    Bruger skabelonen 'tournament/tournament_detail.html'.
    """

    model = Tournament
    template_name = "tournament/tournament_detail.html"
    context_object_name = "tournament"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.object
        brackets = tournament.brackets.all()

        for bracket in brackets:
            bracket.finale_match = bracket.matches.filter(is_finale=True).first()

        context["brackets"] = brackets
        return context


class TournamentScheduleView(DetailView):
    """
    Viser tidsplanen for en specifik turnering.
    Bruger skabelonen 'tournament/tournament_schedule.html'.
    """

    model = Tournament
    template_name = "tournament/tournament_schedule.html"
    context_object_name = "tournament"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.object
        matches = Match.objects.filter(bracket__tournament=tournament).order_by(
            "start_time", "track_number"
        )
        schedule = [
            (
                match.start_time,
                match.track_number,
                match.team1,
                match.team2,
                match.bracket,
                match.group,
                match.winner,
                match.loser,
                match.id,
            )
            for match in matches
        ]
        context["schedule"] = schedule
        return context


def tournament_signup(request, pk):
    """
    Håndterer tilmelding til en specifik turnering.
    Bruger skabelonen 'tournament/tournament_signup.html'.
    """
    tournament = get_object_or_404(Tournament, pk=pk)
    if request.method == "POST":
        form = SignupForm(tournament_id=pk, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("tournament-detail", pk=tournament.pk)
    else:
        form = SignupForm(tournament_id=pk)
    return render(
        request,
        "tournament/tournament_signup.html",
        {"form": form, "tournament": tournament},
    )


@require_GET
def get_tournament_signups(request, pk):
    """
    Viser tilmeldingerne til en specifik turnering.
    Bruger skabelonen 'tournament/tournament_signups.html'.
    """
    tournament = get_object_or_404(Tournament, pk=pk)
    signups = Team.objects.filter(bracket__tournament=tournament)
    return render(
        request,
        "tournament/tournament_signups.html",
        {"signups": signups, "tournament": tournament},
    )
