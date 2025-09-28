# DEPRECATED: Use tests.auth_utils for all authentication utilities
from .auth_utils import (
	AuthUtils,
	authenticate_client,
	get_tokens_for_user,
)

# Backwards-compatible re-exports; keep a minimal public surface so
# static analyzers don't flag wildcard imports elsewhere.
__all__ = ["AuthUtils", "authenticate_client", "get_tokens_for_user"]

# This file is retained for backward compatibility and will be removed in the future.
