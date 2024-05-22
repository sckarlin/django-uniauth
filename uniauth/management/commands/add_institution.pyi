from typing import Any

from django.core.management.base import BaseCommand
from django.core.management.base import CommandParser


class Command(BaseCommand):
    help: str
    def add_arguments(self, parser: CommandParser) -> None: ...
    def handle(self, *args: Any, **options: Any) -> None: ...
