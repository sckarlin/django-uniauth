from typing import Callable, Optional, Any

from uniauth.utils import is_tmp_user as is_tmp_user

def login_required(
        function: Optional[Callable[..., Any]] = None,
        redirect_field_name: str = ...,
        login_url: Optional[str] = None,
) -> Callable[..., Any]: ...
