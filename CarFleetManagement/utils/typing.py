from typing import Any, Optional


def get_user_role_name(user: Any) -> Optional[str]:
    """Return the role name of a custom user if present, else None.

    This helper centralizes runtime checks so type-checker warnings are limited to one place.
    """
    if user is None:
        return None
    if hasattr(user, "role") and user.role is not None:  # type: ignore[attr-defined]
        return user.role.name  # pragma: no cover - trivial runtime guard
    return None
