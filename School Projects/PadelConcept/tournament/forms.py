"""
Denne fil indeholder formularer til Tournament-applikationen.

forms.py bruges til at definere formularer, der håndterer oprettelse og opdatering af modelinstanser via webformularer.
Disse formularer bruges i forskellige views til at indsamle og validere brugerinput.

Indeholder følgende formularer:
1. SignupForm - Bruges til at tilmelde hold til en turnering.
2. MatchResultForm - Bruges til at indrapportere resultater af kampe.
"""

from django import forms
from django.db.models import Count

from .models import Bracket, Match, Team, Tournament


class SignupForm(forms.ModelForm):
    """
    Formular til tilmelding af et hold til en turnering.
    Indeholder felter til spillernavne, kontaktinformation og valg af række.
    """

    player1 = forms.CharField(max_length=200, label="Spiller 1")
    player2 = forms.CharField(max_length=200, label="Spiller 2")
    email = forms.EmailField(max_length=200, label="Email")
    phone = forms.CharField(max_length=200, label="Telefon")
    paid = forms.BooleanField(label="Betalt", required=False)
    bracket = forms.ModelChoiceField(
        queryset=Bracket.objects.none(),
        label="Bracket",
        widget=forms.RadioSelect(),
        required=True,
    )

    class Meta:
        model = Team
        fields = ["player1", "player2", "email", "phone", "bracket", "paid"]

    def __init__(self, tournament_id=None, *args, **kwargs):
        """
        Initialiserer formularen og opsætter queryset for rækker relateret til den valgte turnering.
        """
        super(SignupForm, self).__init__(*args, **kwargs)
        self.tournament = None
        if tournament_id:
            self.tournament = Tournament.objects.filter(pk=tournament_id).first()
            if self.tournament:
                self.fields["bracket"].queryset = Bracket.objects.filter(
                    tournament=self.tournament
                ).annotate(num_teams=Count("teams__bracket"))

                self.fields["bracket"].label_from_instance = (
                    lambda obj: f"{obj} - Pladser {obj.num_teams}/{obj.max_teams}"
                )
            else:
                self.fields["bracket"].queryset = Bracket.objects.none()

    # Gemmer holdet og dets data.
    def save(self, commit=True):
        team_data = {
            "player1": self.cleaned_data["player1"],
            "player2": self.cleaned_data["player2"],
            "email": self.cleaned_data["email"],
            "phone": self.cleaned_data["phone"],
            "bracket": self.cleaned_data["bracket"],
        }
        team, created = Team.objects.get_or_create(
            email=self.cleaned_data["email"], defaults=team_data
        )
        team.save()
        return team

    # Validerer det valgte bracket, og sikrer at det ikke er fuldt.
    def clean_bracket(self):
        bracket = self.cleaned_data.get("bracket")
        if not bracket:
            raise forms.ValidationError("Du skal vælge en række.")

        valid_brackets = self.fields["bracket"].queryset
        if bracket not in valid_brackets:
            raise forms.ValidationError("Denne række er desværre allerede fuld.")

        if (
            bracket.groups.aggregate(total_teams=Count("teams"))["total_teams"]
            >= bracket.max_teams
        ):
            raise forms.ValidationError("Denne række er desværre allerede fuld.")

        return bracket

    # Validerer at betalingsfeltet er markeret.
    def clean_paid(self):
        paid = self.cleaned_data.get("paid")
        if not paid:
            raise forms.ValidationError("Du skal betale for at tilmelde dig.")
        return paid


class MatchResultForm(forms.ModelForm):
    """
    Formular til indrapportering af resultater for en kamp.
    Indeholder felter til at indtaste resultaterne for hvert sæt for begge hold.
    """

    class Meta:
        model = Match
        fields = [
            "team1_set1",
            "team1_set2",
            "team1_set3",
            "team2_set1",
            "team2_set2",
            "team2_set3",
        ]
        widgets = {
            "team1_set1": forms.NumberInput(attrs={"class": "form-control"}),
            "team1_set2": forms.NumberInput(attrs={"class": "form-control"}),
            "team1_set3": forms.NumberInput(attrs={"class": "form-control"}),
            "team2_set1": forms.NumberInput(attrs={"class": "form-control"}),
            "team2_set2": forms.NumberInput(attrs={"class": "form-control"}),
            "team2_set3": forms.NumberInput(attrs={"class": "form-control"}),
        }
