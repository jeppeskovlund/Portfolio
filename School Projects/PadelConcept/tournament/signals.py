"""
Denne fil indeholder signalhåndtering til Tournament-applikationen.

signals.py bruges til at definere og håndtere Django-signaler, som udfører bestemte handlinger, når visse begivenheder sker.
I denne fil håndteres post_save-signaler for at opdatere gruppevindere, når kampe gemmes.

Indeholder følgende signaler:
1. update_group_winner - Opdaterer gruppevinderen og finale-kampe, når en kamp gemmes.
"""

from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from dotenv import load_dotenv  # noqa: F401

from .models import Match
from .templatetags.tournament_extras import group_standings


@receiver(post_save, sender=Match)
def update_group_winner(sender, instance, created, **kwargs):
    """
    Opdaterer gruppevinderen og finale-kampe, når en kamp gemmes.
    """
    if not instance.is_finale:
        group = instance.group

        # Tjek om alle kampe i gruppen er spillet
        if (
            group
            and group.matches.filter(
                Q(winner__isnull=True) & Q(is_finale=False)
            ).count()
            == 0
        ):
            # Hent gruppens stilling
            standings = group_standings(group.id)
            if standings:
                # Det øverste hold i stillingen er gruppevinderen
                group.winner = standings[0]["team"]
                group.save()

                # Find finalekampen for bracketen
                finale_match = group.bracket.matches.filter(is_finale=True).first()
                if finale_match:
                    if group.name == "A":
                        finale_match.team1 = group.winner
                    elif group.name == "B":
                        finale_match.team2 = group.winner
                    finale_match.save()
