from typing import Any

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help: str
    def handle(self, *args: Any, **options: Any) -> None: ...
