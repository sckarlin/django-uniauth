from _typeshed import Incomplete
from typing import Iterable, List, Optional


def merge_model_instances(
        primary_object: Incomplete,
        alias_objects: Iterable[Incomplete],
        field_trace: Optional[List[Incomplete]] = None,
) -> tuple[Incomplete, List[Incomplete], int]: ...
