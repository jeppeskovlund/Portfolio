"""
Denne fil indeholder tests for Tournament-applikationen.

tests.py bruges til at definere enhedstests og integrationstests for at sikre, at applikationen fungerer korrekt.
Tests inkluderer modeltests, formular-tests, view-tests og URL-resolutions tests.

Indeholder følgende testklasser:
1. LocationModelTests - Tester oprettelse og funktionalitet af Location-modellen.
2. TournamentModelTests - Tester oprettelse og funktionalitet af Tournament-modellen.
3. SignupFormTests - Tester validering af tilmeldingsformularen.
4. MatchResultFormTests - Tester validering af match-resultatformularen.
5. TournamentViewTests - Tester forskellige views relateret til turneringer.
6. TournamentURLTests - Tester URL-opløsning for forskellige turnerings-relaterede views.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import MatchResultForm, SignupForm
from .models import Bracket, Group, Location, Match, Team, Tournament


# Tester oprettelse og funktionalitet af lokationer.
class LocationModelTests(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            name="Padel Lounge", address="Street 123", city="Copenhagen", zip_code=2200
        )

    # Tester om en lokation oprettes korrekt.
    def test_location_creation(self):
        self.assertIsInstance(self.location, Location)
        self.assertEqual(self.location.name, "Padel Lounge")
        self.assertEqual(self.location.city, "Copenhagen")


# Tester oprettelse og funktionalitet af turneringer.
class TournamentModelTests(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            name="Padel Lounge", address="Street 123", city="Copenhagen", zip_code=2200
        )
        self.tournament = Tournament.objects.create(
            name="Summer Open",
            date="2023-06-01",
            start_time="15:00:00",
            end_time="23:59:59",
            tracks=6,
            location=self.location,
        )

    # Tester om en turnering oprettes korrekt.
    def test_tournament_creation(self):
        self.assertIsInstance(self.tournament, Tournament)
        self.assertEqual(self.tournament.name, "Summer Open")
        self.assertEqual(self.tournament.location, self.location)


# Tester validering af tilmeldingsformularen.
class SignupFormTests(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            name="Padel Lounge", address="Street 123", city="Copenhagen", zip_code=2200
        )
        self.tournament = Tournament.objects.create(
            name="Summer Open",
            date="2023-06-01",
            start_time="15:00:00",
            end_time="23:59:59",
            tracks=6,
            location=self.location,
        )
        self.bracket = Bracket.objects.create(
            tournament=self.tournament,
            level_from=1,
            level_to=2,
            name="Bracket A",
            max_teams=8,
        )

    # Tester om tilmeldingsformularen er gyldig med korrekt data.
    def test_signup_form_valid(self):
        form_data = {
            "player1": "Player One",
            "player2": "Player Two",
            "email": "team@example.com",
            "phone": "12345678",
            "bracket": self.bracket.id,
            "paid": True,
        }
        form = SignupForm(tournament_id=self.tournament.id, data=form_data)
        self.assertTrue(form.is_valid())

    # Tester om tilmeldingsformularen er ugyldig med manglende data.
    def test_signup_form_invalid(self):
        form_data = {
            "player1": "",
            "player2": "Player Two",
            "email": "team@example.com",
            "phone": "12345678",
            "bracket": self.bracket.id,
            "paid": True,
        }
        form = SignupForm(tournament_id=self.tournament.id, data=form_data)
        self.assertFalse(form.is_valid())


# Tester validering af match resultat formularen.
class MatchResultFormTests(TestCase):
    def test_match_result_form_valid(self):
        """
        Tester om match-resultatformularen er gyldig med korrekt data.
        """
        form_data = {
            "team1_set1": 6,
            "team1_set2": 4,
            "team1_set3": 6,
            "team2_set1": 4,
            "team2_set2": 6,
            "team2_set3": 4,
        }
        form = MatchResultForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Tester om match-resultatformularen er ugyldig med forkert data.
    def test_match_result_form_invalid(self):
        form_data = {
            "team1_set1": 6,
            "team1_set2": 4,
            "team1_set3": 6,
            "team2_set1": 4,
            "team2_set2": 6,
            "team2_set3": "invalid",  # Ugyldig data
        }
        form = MatchResultForm(data=form_data)
        self.assertFalse(form.is_valid())


# Tester forskellige views relateret til turneringer.
class TournamentViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="admin")
        self.user.is_staff = True  # Gør brugeren til en medarbejder
        self.user.save()
        self.client.login(username="admin", password="admin")
        self.location = Location.objects.create(
            name="Padel Lounge", address="Street 123", city="Copenhagen", zip_code=2200
        )
        self.tournament = Tournament.objects.create(
            name="Summer Open",
            date="2023-06-01",
            start_time="15:00:00",
            end_time="23:59:59",
            tracks=6,
            location=self.location,
        )

    # Tester om index-viewet returnerer statuskode 200.
    def test_index_view_status_code(self):
        url = reverse("tournament-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # Tester om index-viewet bruger den korrekte skabelon.
    def test_index_view_template(self):
        url = reverse("tournament-list")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "index.html")

    # Tester om tournament-detail-viewet fungerer korrekt.
    def test_tournament_detail_view(self):
        url = reverse("tournament-detail", kwargs={"pk": self.tournament.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tournament/tournament_detail.html")

    # Tester om tournament-signup-viewet fungerer korrekt.
    def test_tournament_signup_view(self):
        url = reverse("tournament-signup", kwargs={"pk": self.tournament.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tournament/tournament_signup.html")

    # Tester om match-resultatformular-viewet fungerer korrekt.
    def test_match_result_form_view(self):
        bracket = Bracket.objects.create(
            tournament=self.tournament,
            level_from=1,
            level_to=2,
            name="Bracket A",
            max_teams=8,
        )
        group = Group.objects.create(bracket=bracket, name="A")
        team1 = Team.objects.create(
            player1="Player One",
            player2="Player Two",
            email="team1@example.com",
            phone="12345678",
            bracket=bracket,
        )
        team2 = Team.objects.create(
            player1="Player Three",
            player2="Player Four",
            email="team2@example.com",
            phone="87654321",
            bracket=bracket,
        )
        match = Match.objects.create(
            group=group,
            bracket=bracket,
            team1=team1,
            team2=team2,
        )

        url = reverse("match-result-form", kwargs={"match_id": match.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tournament/match_result_form.html")
