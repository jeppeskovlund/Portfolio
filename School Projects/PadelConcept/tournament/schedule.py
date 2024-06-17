"""
Denne fil indeholder funktionalitet til at generere en tidsplan for en turnering.

schedule.py bruges til at planlægge kampe for en turnering, så de spilles på de rigtige tidspunkter og baner.
Funktionen `generate_schedule` håndterer planlægning af gruppekampe og finalekampe, sikrer at hold ikke spiller
flere kampe i samme runde, og fordeler kampene på de tilgængelige baner.

Indeholder følgende funktion:
1. generate_schedule - Genererer en tidsplan for en turnering baseret på turneringens dato, starttid, antal baner og kampe.
"""

from collections import defaultdict
from datetime import datetime, timedelta

from django.utils import timezone

from .models import Match


def generate_schedule(tournament):
    """
    Genererer en tidsplan for en given turnering.
    Planlægger kampe for de forskellige brackets og grupper, og tildeler starttider og baner.
    """
    start_time = timezone.make_aware(
        datetime.combine(tournament.date, tournament.start_time)
    )
    match_duration = timedelta(minutes=50)
    number_of_tracks = tournament.tracks
    rounds = defaultdict(list)  # Dictionary til at holde styr på runder
    bracket_match_counts = defaultdict(
        int
    )  # Sporer antallet af gruppekampe per bracket
    bracket_match_scheduled = defaultdict(
        int
    )  # Sporer antallet af planlagte gruppekampe per bracket

    # Henter alle kampe og gruppér efter bracket og gruppe
    group_matches = Match.objects.filter(
        bracket__tournament=tournament, is_finale=False
    ).order_by("group__bracket", "group")
    final_matches = Match.objects.filter(bracket__tournament=tournament, is_finale=True)

    # Tæller antallet af gruppekampe for hver bracket
    for match in group_matches:
        bracket_match_counts[match.bracket] += 1

    current_round = 1
    finals_ready = []

    # Tildeler gruppekampe til runder
    while group_matches.exists():
        matches_in_round = []
        teams_played_in_current_round = set()
        brackets_played_in_current_round = set()

        for match in group_matches:
            if finals_ready:
                if finals_ready[0][1] not in brackets_played_in_current_round:
                    matches_in_round.append((current_round, finals_ready[0][0]))
                    finals_ready.pop(0)
            # Sørger for, at et hold ikke spiller to kampe i samme runde
            if (
                match.team1 not in teams_played_in_current_round
                and match.team2 not in teams_played_in_current_round
            ):
                matches_in_round.append((current_round, match))
                teams_played_in_current_round.add(match.team1)
                teams_played_in_current_round.add(match.team2)
                brackets_played_in_current_round.add(match.bracket)
                group_matches = group_matches.exclude(pk=match.pk)
                bracket_match_scheduled[match.bracket] += 1
            if (
                bracket_match_scheduled[match.bracket]
                == bracket_match_counts[match.bracket]
            ):
                # Alle gruppekampe er planlagt
                # Tilføjer finalekampe til tidsplanen
                final_match = final_matches.filter(bracket=match.bracket).first()
                finals_ready.append([final_match, match.bracket])

            if len(matches_in_round) == number_of_tracks:
                break

        rounds[current_round].extend(matches_in_round)
        current_round += 1

    # Tilføjer de sidste finalekampe når der ikke er flere gruppekampe.
    if finals_ready:
        for match in finals_ready:
            matches_in_round = []
            matches_in_round.append((current_round, match[0]))
            rounds[current_round].extend(matches_in_round)

    # Tildeler starttid og bane til hver kamp i tidsplanen
    schedule = []
    for round_number, matches in sorted(rounds.items()):
        for i, (round_number, match) in enumerate(matches):
            match_start_time = start_time + (round_number - 1) * match_duration
            match.track_number = (i % number_of_tracks) + 1
            match.start_time = match_start_time
            match.save()
            schedule.append((round_number, match, match_start_time, match.track_number))

    return schedule
