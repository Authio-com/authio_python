"""Authio — passwordless, multi-org auth for B2B apps.

A user identity belongs to many organizations. ``Session.user_id`` is the
person; ``Session.org_id`` is the active organization context (may be
``None`` if the user authenticated but has not yet selected an org).
"""

from .client import Authio, AuthioError
from .types import Membership, MembershipStatus, Organization, Session, User

__all__ = [
    "Authio",
    "AuthioError",
    "Membership",
    "MembershipStatus",
    "Organization",
    "Session",
    "User",
]

__version__ = "0.1.0a0"
