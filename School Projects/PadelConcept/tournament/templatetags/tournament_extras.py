"""
Denne fil indeholder brugerdefinerede template tags til Tournament-applikationen.

templatetags.py bruges til at definere funktioner, der kan bruges direkte i Django-templates for at udføre specifikke logikker,
som beregning af stillinger og kampresultater.

Indeholder følgende funktioner:
1. matches_won - Returnerer antallet af vundne kampe for et hold.
2. matches_lost - Returnerer antallet af tabte kampe for et hold.
3. sets_won - Returnerer antallet af vundne sæt for et hold.
4. sets_lost - Returnerer antallet af tabte sæt for et hold.
5. points_won - Returnerer antallet af vundne point for et hold.
6. points_lost - Returnerer antallet af tabte point for et hold.
7. set_difference - Beregner forskellen mellem vundne og tabte sæt for et hold.
8. point_difference - Beregner forskellen mellem vundne og tabte point for et hold.
9. group_standings - Returnerer stillingen for en gruppe baseret på vundne kampe, sætforskel og pointforskel.
10. finale_ready - Tjekker om en bracket er klar til finalen, dvs. om begge hold til finalen er sat.
"""

from django import template
from django.db.models import Q

from tournament.models import Group

register = template.Library()


# Returnerer antallet af vundne kampe for et hold.
def matches_won(team):
    return team.won_matches.filter(is_finale=False).count()


# Returnerer antallet af tabte kampe for et hold.
def matches_lost(team):
    return team.lost_matches.filter(is_finale=False).count()


# Returnerer antallet af vundne sæt for et hold.
def sets_won(team):
    return (
        team.won_set1.filter(is_finale=False).count()
        + team.won_set2.filter(is_finale=False).count()
        + team.won_set3.filter(is_finale=False).count()
    )


# Returnerer antallet af tabte sæt for et hold.
def sets_lost(team):
    return (
        team.lost_set1.filter(is_finale=False).count()
        + team.lost_set2.filter(is_finale=False).count()
        + team.lost_set3.filter(is_finale=False).count()
    )


# Returnerer antallet af vundne point for et hold.
def points_won(team):
    total = 0
    for match in team.won_matches.filter(is_finale=False):
        total += match.get_game_points(team)[0]
    for match in team.lost_matches.filter(is_finale=False):
        total += match.get_game_points(team)[0]
    return total


# Returnerer antallet af tabte point for et hold.
def points_lost(team):
    total = 0
    for match in team.won_matches.filter(is_finale=False):
        total += match.get_game_points(team)[1]
    for match in team.lost_matches.filter(is_finale=False):
        total += match.get_game_points(team)[1]
    return total


# Beregner forskellen mellem vundne og tabte sæt for et hold.
def set_difference(team):
    return sets_won(team) - sets_lost(team)


# Beregner forskellen mellem vundne og tabte point for et hold.
def point_difference(team):
    return points_won(team) - points_lost(team)


# Returnerer stillingen for en gruppe baseret på vundne kampe, sætforskel og pointforskel.
# Decorator simple_tag så ved brug af 'group_standings' i en template, vil denne funktion blive kaldt.
@register.simple_tag
def group_standings(group_id):
    group = Group.objects.get(pk=group_id)
    teams = group.teams.all()
    standings = []
    for team in teams:
        standings.append(
            {
                "team": team,
                "matches_won": matches_won(team),
                "matches_lost": matches_lost(team),
                "sets_won": sets_won(team),
                "sets_lost": sets_lost(team),
                "points_won": points_won(team),
                "points_lost": points_lost(team),
                "set_difference": set_difference(team),
                "point_difference": point_difference(team),
            }
        )
    return sorted(
        standings,
        key=lambda x: (x["matches_won"], x["set_difference"], x["point_difference"]),
        reverse=True,
    )


# Tjekker om en bracket er klar til finalen, dvs. om begge hold til finalen er sat.
# Decorator simple_tag så ved brug af 'finale_ready' i en template, vil denne funktion blive kaldt.
@register.simple_tag
def finale_ready(bracket):
    return bracket.matches.filter(
        Q(team1__isnull=False) & Q(team2__isnull=False) & Q(is_finale=True)
    )
