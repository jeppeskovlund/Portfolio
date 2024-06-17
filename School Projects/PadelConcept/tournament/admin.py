"""
Admin-konfigurationsfil for Padel Concept-projektet.

Denne fil konfigurerer admin-interface for de forskellige modeller i Padel Concept-projektet.
Den bruger Django's admin-framework til at tilføje, redigere og slette objekter i databasen via et brugervenligt web-interface.

Indeholder følgende konfigurationer:
1. Tilpassede formsets og inline-klasser til Bracket-modellen.
2. Inline-klasser til Team og Match modellerne for at håndtere relaterede objekter.
3. Tilpassede admin-klasser til håndtering af Tournament, Match, Group, Location, Bracket og Team modellerne.
4. Brugerdefinerede handlinger for oprettelse af tidsplaner og grupper/matcher.
5. Brugerdefinerede filtre for nemmere navigation og administration af data.

Hovedfunktioner:
- Opret og rediger turneringer, brackets, hold, kampe og lokationer.
- Generer automatisk tidsplaner og kampe for turneringer.
- Tilbyder avancerede filtre for bedre søgning og filtrering i admin-interface.
"""

from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

from .models import Bracket, Group, Location, Match, Team, Tournament
from .schedule import generate_schedule


class BracketInlineFormSet(BaseInlineFormSet):
    """
    En tilpasset formset-klasse til BracketInline-modellen.
    Denne klasse udvider BaseInlineFormSet og tilføjer funktionalitet til initialisering af formsettet.
    Bruges til at tilføje standard brackets til oprettelse af en ny turnering.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk and not self.data:
            default_brackets = ["Øvet", "Let Øvet A", "Let Øvet B", "Begynder", "Mix"]
            default_level_from = [3.0, 2.5, 2.0, 1.5, 1.5]
            default_level_to = [3.5, 2.9, 2.5, 2.0, 3.0]
            self.initial = [
                {
                    "name": name,
                    "level_from": default_level_from[index],
                    "level_to": default_level_to[index],
                    "max_teams": 8,
                }
                for index, name in enumerate(default_brackets)
            ]
            self.extra = len(self.initial)


class BracketInline(admin.TabularInline):
    """
    En inline-administrator tilknyttet Bracket-modellen.
    Denne klasse bruges til at vise og redigere Bracket-objekter i en tabulær formular i adminpanelet.
    Det er en del af admin-interfacet for Tournament-modellen.
    """

    model = Bracket
    extra = 0
    formset = BracketInlineFormSet
    fields = ["name", "level_from", "level_to"]
    verbose_name = "Bracket"
    verbose_name_plural = "Brackets"


class TeamInline(admin.TabularInline):
    """
    En inline-administrator tilknyttet Team-modellen.
    Denne klasse bruges til at vise og redigere Team-objekter i en tabulær formular i adminpanelet.
    Det er en del af admin-interfacet for Group-modellen.
    """

    model = Team
    extra = 1


class MatchInline(admin.TabularInline):
    """
    En inline-administrator tilknyttet Match-modellen.
    Denne klasse bruges til at vise og redigere Match-objekter i admin-interfacet.
    Det er en del af admin-interfacet for Group-modellen.
    """

    model = Match
    extra = 1
    fields = ["team1", "team2", "is_finale"]


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    """
    En brugerdefineret admin-klasse til Tournament-modellen.
    Denne klasse definerer forskellige egenskaber og handlinger for admin-interfacet.
    """

    inlines = [BracketInline]
    actions = ["create_schedule", "create_groups_and_matches"]
    list_display = ["name", "date", "start_time", "location", "tracks"]
    list_filter = ["location"]
    search_fields = ["name", "location__name", "date"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

    def create_schedule(self, request, queryset):
        """
        En handling til at oprette en tidsplan for valgte turneringer.
        Denne handling genererer en tidsplan ved hjælp af funktionen generate_schedule.
        """
        # Opretter tidsplan for hver valgte turnering
        for tournament in queryset:
            generate_schedule(tournament)
        # Sender besked til admin panelet
        self.message_user(request, "Tidsplan oprettet for valgte turneringer")

    def create_groups_and_matches(self, request, queryset):
        """
        En handling til at oprette grupper og kampe for valgte turneringer.
        Denne handling opretter grupper og kampe ved hjælp af forskellige logikker og filtre.
        """
        # Opretter grupper og kampe for hver turnering der er valgt
        for tournament in queryset:
            brackets = Bracket.objects.filter(tournament=tournament)
            for bracket in brackets:
                group_a = Group.objects.create(bracket=bracket, name="A")
                group_b = Group.objects.create(bracket=bracket, name="B")
                teams = Team.objects.filter(bracket=bracket)
                # Deler holdene op i to grupper
                teams_a = teams[: len(teams) // 2]
                teams_b = teams[len(teams) // 2 :]

                for team in teams:
                    team.group = group_a if team in teams_a else group_b
                    team.save()

                # Opretter 'round-robin' kampe for gruppe A
                for first in range(len(teams_a)):
                    for second in range(first + 1, len(teams_a)):
                        Match.objects.create(
                            group=group_a,
                            bracket=bracket,
                            team1=teams_a[first],
                            team2=teams_a[second],
                        )

                # Opretter 'round-robin' kampe for gruppe B
                for first in range(len(teams_b)):
                    for second in range(first + 1, len(teams_b)):
                        Match.objects.create(
                            group=group_b,
                            bracket=bracket,
                            team1=teams_b[first],
                            team2=teams_b[second],
                        )
                # Opretter finalekamp for rækken
                Match.objects.create(bracket=bracket, is_finale=True)
        # Sender besked til admin panelet
        self.message_user(request, "Grupper og kampe oprettet for valgte turneringer")

    create_schedule.short_description = "Opret tidsplan"
    create_groups_and_matches.short_description = "Opret grupper og kampe"


class TournamentFilter(admin.SimpleListFilter):
    """
    Dette filter giver mulighed for at filtrere objekter baseret på tilhørende turneringer.
    Bruges i MatchAdmin hvor der ikke er en direkte relation til Tournament.
    """

    title = _("tournament")
    parameter_name = "tournament"

    def lookups(self, request, model_admin):
        tournaments = set(Tournament.objects.all())
        return [(t.id, t.name) for t in tournaments]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(bracket__tournament__id=self.value())
        return queryset


class BracketFilter(admin.SimpleListFilter):
    """
    Filteret kigger på navn i stedet for ID som ellers er standard.
    Derfor er et brugerdefineret filter nødvendigt for at undgå duplikationer.
    """

    title = _("bracket")
    parameter_name = "bracket"

    def lookups(self, request, model_admin):
        brackets = Bracket.objects.values_list("name", flat=True).distinct()
        return [(b, b) for b in brackets]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(bracket__name=self.value())
        return queryset


class GroupFilter(admin.SimpleListFilter):
    """
    Filteret kigger på navn i stedet for ID som ellers er standard.
    Derfor er et brugerdefineret filter nødvendigt for at undgå duplikationer.
    """

    title = _("bracket")
    parameter_name = "bracket"

    def lookups(self, request, model_admin):
        brackets = Group.objects.values_list("name", flat=True).distinct()
        return [(b, b) for b in brackets]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(bracket__name=self.value())
        return queryset


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    """
    Adminpanel adgang til kampene for at kunne rette og indrapportere resultater.
    Dette gøres nu ved 'match_result_form', men denne beholdes som backup.
    """

    list_display = ["match_str", "is_finale", "group", "bracket", "match_tournament"]
    list_filter = ["is_finale", GroupFilter, BracketFilter, TournamentFilter]
    fields = [
        ("team1", "team1_set1", "team1_set2", "team1_set3"),
        ("team2", "team2_set1", "team2_set2", "team2_set3"),
    ]

    def match_str(self, obj):
        return str(obj)

    def match_tournament(self, obj):
        return obj.bracket.tournament

    match_str.short_description = "Match"
    match_tournament.short_description = "Tournament"


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """
    Adminpanel adgang til kampene for at kunne rette og sletter grupper.
    Oprettelse sker ved at turnering kører funktionen 'create_groups_and_matches'.
    """

    inlines = [TeamInline, MatchInline]
    list_display = ["group_str", "group_tournament"]
    list_filter = [BracketFilter, TournamentFilter]

    def group_str(self, obj):
        return str(obj)

    def group_tournament(self, obj):
        return obj.bracket.tournament

    group_str.short_description = "Group"
    group_tournament.short_description = "Tournament"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    Adminpanel adgang til at oprette og redigere lokationer.
    """

    list_display = ("name", "address", "city", "zip_code")
    search_fields = ("name", "address", "city", "zip_code")
    list_filter = ("zip_code", "city")


@admin.register(Bracket)
class BracketAdmin(admin.ModelAdmin):
    """
    Adminpanel adgang til at redigere og slette brackets.
    Oprettelse sker ved oprettelse af en turnering.
    """

    list_display = ["name", "level_from", "level_to", "tournament"]
    list_filter = ["name", "level_from", "level_to", "tournament"]
    search_fields = ["name", "level_from", "level_to", "tournament"]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """
    Adminpanel adgang til at redigere og slette hold.
    Oprettelse sker ved tilmeldning til turneringerne.
    """

    list_display = ["team_str", "group", "bracket", "team_tournament"]
    list_filter = [GroupFilter, BracketFilter, TournamentFilter]
    search_fields = ["player1", "player2", "email", "phone"]

    def team_str(self, obj):
        return str(obj)

    def team_tournament(self, obj):
        return obj.bracket.tournament

    team_tournament.short_description = "Tournament"
    team_str.short_description = "Team"
