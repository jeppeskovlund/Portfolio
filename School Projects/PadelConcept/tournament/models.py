"""
Denne fil indeholder modeldefinitioner til Tournament-applikationen.

models.py bruges til at definere databasemodeller, som repræsenterer de forskellige entiteter i applikationen.
Hver modelklasse svarer til en tabel i databasen og indeholder felter, der repræsenterer kolonner i tabellen,
samt metoder til at manipulere dataene.

Indeholder følgende modeller:
1. Location - Repræsenterer en lokation, hvor turneringer afholdes.
2. Tournament - Repræsenterer en turnering med specifikke detaljer som dato, tid og lokation.
3. Bracket - Repræsenterer en række inden for en turnering, med niveauer og maksimalt antal hold.
4. Group - Repræsenterer en gruppe inden for en bracket.
5. Team - Repræsenterer et hold med to spillere, kontaktinformation og tilknytning til en bracket og en gruppe.
6. Match - Repræsenterer en kamp mellem to hold med resultater for hvert sæt.
"""

import calendar
from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Location(models.Model):
    """
    Model, der repræsenterer en lokation, hvor turneringer afholdes.
    Indeholder felter for navn, adresse, by og postnummer.
    """

    name = models.CharField("Navn", default="Padel Lounge", max_length=200, unique=True)
    address = models.CharField("Adresse", max_length=200)
    city = models.CharField("By", max_length=200)
    zip_code = models.IntegerField(
        "Postnummer",
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(9999),
        ],
    )

    def __str__(self):
        return f"{self.name} ({self.address}, {self.zip_code} {self.city})"

    class Meta:
        verbose_name = "Lokation"
        verbose_name_plural = "Lokationer"


# Dansk oversættelse af måneder
months = {
    "January": "Januar",
    "February": "Februar",
    "March": "Marts",
    "April": "April",
    "May": "Maj",
    "June": "Juni",
    "July": "Juli",
    "August": "August",
    "September": "September",
    "October": "Oktober",
    "November": "November",
    "December": "December",
}
# Standardnavn for turneringer
default_name = f"Fredagsturnering {months.get(calendar.month_name[date.today().month + 1])} {date.today().year} Aalborg"


class Tournament(models.Model):
    """
    Model, der repræsenterer en turnering.
    Indeholder felter for navn, dato, starttid, sluttid, antal baner og lokation.
    """

    name = models.CharField("Navn", max_length=200, default=default_name, unique=True)
    date = models.DateField("Dato")
    start_time = models.TimeField("Start", default="15:00:00")
    end_time = models.TimeField("Slut", default="23:59:59")
    tracks = models.IntegerField("Antal Baner", default=6)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        verbose_name="Lokation",
        null=True,
        default=1,
    )

    class Meta:
        verbose_name = "Turnering"
        verbose_name_plural = "Turneringer"
        ordering = ["date"]

    def __str__(self):
        return f"{self.name} ({self.date})"

    def get_absolute_url(self):
        return reverse("tournament-detail", kwargs={"pk": self.pk})


class Bracket(models.Model):
    """
    Model, der repræsenterer en række inden for en turnering.
    Indeholder felter for niveauer, navn og maksimalt antal hold.
    """

    tournament = models.ForeignKey(
        Tournament, related_name="brackets", on_delete=models.CASCADE
    )
    level_from = models.DecimalField(max_digits=2, decimal_places=1, default=1)
    level_to = models.DecimalField(max_digits=2, decimal_places=1, default=2)
    name = models.CharField(max_length=100, default="Bracket")
    max_teams = models.IntegerField(default=8)

    def __str__(self):
        return f"{self.name}"

    def get_final_match(self):
        """
        Returnerer finalekampen for denne række.
        """
        return Match.objects.filter(group__bracket=self, is_finale=True).first()

    class Meta:
        verbose_name = "Række"
        verbose_name_plural = "Rækker"


class Group(models.Model):
    """
    Model, der repræsenterer en gruppe inden for en bracket.
    Indeholder felter for navn og vinder.
    """

    bracket = models.ForeignKey(
        Bracket, related_name="groups", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=1)  # 'A' or 'B'
    winner = models.ForeignKey(
        "Team",
        related_name="won_groups",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"{self.bracket} - {self.name}"

    class Meta:
        verbose_name = "Gruppe"
        verbose_name_plural = "Grupper"


class Team(models.Model):
    """
    Model, der repræsenterer et hold med to spillere.
    Indeholder felter for spillernavne, email, telefon, betalingsstatus,
    tilknytning til en gruppe og en række.
    """

    player1 = models.CharField(max_length=200)
    player2 = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=200)
    paid = models.BooleanField(default=False)
    group = models.ForeignKey(
        Group, related_name="teams", on_delete=models.SET_NULL, null=True, blank=True
    )
    bracket = models.ForeignKey(Bracket, related_name="teams", on_delete=models.CASCADE)

    def __str__(self):
        player1_names = self.player1.split()
        player2_names = self.player2.split()
        player1_initials = " ".join(
            [f"{name[0].upper()}." for name in player1_names[1:]]
        )
        player2_initials = " ".join(
            [f"{name[0].upper()}." for name in player2_names[1:]]
        )
        return f"{player1_names[0]} {player1_initials} / {player2_names[0]} {player2_initials}"

    class Meta:
        verbose_name = "Hold"
        verbose_name_plural = "Hold"


class Match(models.Model):
    """
    Model, der repræsenterer en kamp mellem to hold.
    Indeholder felter for resultater for hvert sæt, starttid, banenummer,
    vinder og taber af hver kamp og sæt.
    """

    group = models.ForeignKey(
        Group, related_name="matches", on_delete=models.CASCADE, null=True, blank=True
    )
    bracket = models.ForeignKey(
        Bracket, related_name="matches", on_delete=models.CASCADE, null=True, blank=True
    )
    team1 = models.ForeignKey(
        Team,
        related_name="home_matches",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    team2 = models.ForeignKey(
        Team,
        related_name="away_matches",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_finale = models.BooleanField(default=False)
    team1_set1 = models.IntegerField("Sæt 1", default=0)
    team1_set2 = models.IntegerField("Sæt 2", default=0)
    team1_set3 = models.IntegerField("Sæt 3", default=0)
    team2_set1 = models.IntegerField("Sæt 1", default=0)
    team2_set2 = models.IntegerField("Sæt 2", default=0)
    team2_set3 = models.IntegerField("Sæt 3", default=0)

    winner_set1 = models.ForeignKey(
        Team, related_name="won_set1", on_delete=models.CASCADE, null=True, blank=True
    )
    winner_set2 = models.ForeignKey(
        Team, related_name="won_set2", on_delete=models.CASCADE, null=True, blank=True
    )
    winner_set3 = models.ForeignKey(
        Team, related_name="won_set3", on_delete=models.CASCADE, null=True, blank=True
    )
    loser_set1 = models.ForeignKey(
        Team, related_name="lost_set1", on_delete=models.CASCADE, null=True, blank=True
    )
    loser_set2 = models.ForeignKey(
        Team, related_name="lost_set2", on_delete=models.CASCADE, null=True, blank=True
    )
    loser_set3 = models.ForeignKey(
        Team, related_name="lost_set3", on_delete=models.CASCADE, null=True, blank=True
    )
    team1_points = models.IntegerField(default=0)
    team2_points = models.IntegerField(default=0)
    winner = models.ForeignKey(
        Team,
        related_name="won_matches",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    loser = models.ForeignKey(
        Team,
        related_name="lost_matches",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    start_time = models.DateTimeField(null=True, blank=True)
    track_number = models.IntegerField(null=True, blank=True)

    # Returnerer antallet af point for et givet hold i denne kamp.
    def get_game_points(self, team):
        if self.team1 == team:
            return [
                self.team1_set1 + self.team1_set2 + self.team1_set3,
                self.team2_set1 + self.team2_set2 + self.team2_set3,
            ]
        else:
            return [
                self.team2_set1 + self.team2_set2 + self.team2_set3,
                self.team1_set1 + self.team1_set2 + self.team1_set3,
            ]

    # Gemmer kampen og opdaterer kampresultaterne før gemning.
    def save(self, *args, **kwargs):
        self.update_match_results()
        super().save(*args, **kwargs)

    def update_match_results(self):
        """
        Opdaterer resultaterne af kampen, bestemmer vindere og tabere af hver sæt og kampen.
        """
        # Bestem sæt-vindere
        if self.team1_set1 > self.team2_set1:
            self.winner_set1 = self.team1
            self.loser_set1 = self.team2
        elif self.team1_set1 < self.team2_set1:
            self.winner_set1 = self.team2
            self.loser_set1 = self.team1
        else:
            self.winner_set1 = None
            self.loser_set1 = None

        if self.team1_set2 > self.team2_set2:
            self.winner_set2 = self.team1
            self.loser_set2 = self.team2
        elif self.team1_set2 < self.team2_set2:
            self.winner_set2 = self.team2
            self.loser_set2 = self.team1
        else:
            self.winner_set2 = None
            self.loser_set2 = None

        if self.team1_set3 > self.team2_set3:
            self.winner_set3 = self.team1
            self.loser_set3 = self.team2
        elif self.team1_set3 < self.team2_set3:
            self.winner_set3 = self.team2
            self.loser_set3 = self.team1
        else:
            self.winner_set3 = None
            self.loser_set3 = None

        # Bestem kamp-vinderen
        team1_wins = sum(
            [
                self.winner_set1 == self.team1,
                self.winner_set2 == self.team1,
                self.winner_set3 == self.team1,
            ]
        )
        team2_wins = sum(
            [
                self.winner_set1 == self.team2,
                self.winner_set2 == self.team2,
                self.winner_set3 == self.team2,
            ]
        )

        if team1_wins > team2_wins:
            self.winner = self.team1
            self.loser = self.team2
        elif team2_wins > team1_wins:
            self.winner = self.team2
            self.loser = self.team1
        else:
            self.winner = None
            self.loser = None

        self.team1_points = self.team1_set1 + self.team1_set2 + self.team1_set3
        self.team2_points = self.team2_set1 + self.team2_set2 + self.team2_set3

    def __str__(self):
        return f"{self.team1} vs {self.team2}"

    class Meta:
        verbose_name = "Kamp"
        verbose_name_plural = "Kampe"
