"""
Denne fil konfigurerer Tournament-applikationen.

apps.py bruges til at definere konfigurationen af applikationen, såsom dens navn og eventuelle opstartslogik.
Det er også her, hvor vi kan tilføje initialiseringskode, som skal køres, når applikationen starter,
for eksempel til registrering af signaler.
"""

from django.apps import AppConfig


class TournamentConfig(AppConfig):
    """
    Konfigurationsklasse for Tournament-applikationen.
    Definerer standard indstillinger og importerer signaler ved opstart.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "tournament"

    def ready(self):
        """
        Kører startkode for applikationen.
        Importerer signaler for at sikre, at de registreres ved opstart.
        """
        import tournament.signals  # noqa: F401
