from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

MembershipStatus = Literal["invited", "active", "suspended", "deactivated"]


@dataclass
class User:
    id: str
    project_id: str
    email: str
    email_verified: bool
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    default_organization_id: Optional[str] = None


@dataclass
class Organization:
    id: str
    project_id: str
    name: str
    slug: str


@dataclass
class Membership:
    id: str
    project_id: str
    user_id: str
    organization_id: str
    role: str
    status: MembershipStatus
    preferred_login_method: Optional[
        Literal["passkey", "magic_link", "oauth", "sso"]
    ] = None


@dataclass
class Session:
    """Verified session.

    ``user_id`` always identifies the person. ``org_id`` is the active
    organization, or ``None`` when the user has authenticated but not yet
    selected an org (multi-org users).
    """

    session_id: str
    user_id: str
    org_id: Optional[str] = None
    role: Optional[str] = None
