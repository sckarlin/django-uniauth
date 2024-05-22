from django.db import migrations


class Migration(migrations.Migration):
    initial: bool | None = None
    dependencies: list[migrations.migration.SwappableTuple]
    operations: list[migrations.operations.models.ModelOperation]
