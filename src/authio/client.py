from __future__ import annotations

from dataclasses import asdict
from typing import Any
from urllib.parse import quote

import httpx

from .types import Membership, Organization, Session, User


class AuthioError(Exception):
    def __init__(self, code: str, message: str, status: int, request_id: str | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.request_id = request_id


class Authio:
    """Authio Python server SDK."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.authio.com",
        client: httpx.Client | None = None,
    ) -> None:
        if not api_key:
            raise ValueError("Authio: api_key is required")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._http = client or httpx.Client(timeout=30.0)

    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------

    def get_user(self, user_id: str) -> User:
        data = self._request("GET", f"/v1/users/{_seg(user_id)}")
        return User(**_keep(data, User))

    def list_memberships(self, user_id: str) -> list[Membership]:
        rows = self._request("GET", f"/v1/users/{_seg(user_id)}/memberships") or []
        return [Membership(**_keep(r, Membership)) for r in rows]

    # ------------------------------------------------------------------
    # Organizations
    # ------------------------------------------------------------------

    def list_organizations(self) -> list[Organization]:
        rows = self._request("GET", "/v1/organizations") or []
        return [Organization(**_keep(r, Organization)) for r in rows]

    def create_organization(
        self, *, name: str, slug: str | None = None, domain: str | None = None
    ) -> Organization:
        body: dict[str, Any] = {"name": name}
        if slug:
            body["slug"] = slug
        if domain:
            body["domain"] = domain
        data = self._request("POST", "/v1/organizations", body)
        return Organization(**_keep(data, Organization))

    # ------------------------------------------------------------------
    # Memberships
    # ------------------------------------------------------------------

    def add_member(self, organization_id: str, *, user_id: str, role: str) -> Membership:
        data = self._request(
            "POST",
            f"/v1/organizations/{_seg(organization_id)}/memberships",
            {"user_id": user_id, "role": role},
        )
        return Membership(**_keep(data, Membership))

    def remove_member(self, organization_id: str, membership_id: str) -> None:
        self._request(
            "DELETE",
            f"/v1/organizations/{_seg(organization_id)}/memberships/{_seg(membership_id)}",
        )

    # ------------------------------------------------------------------
    # Sessions
    # ------------------------------------------------------------------

    def switch_org(self, organization_id: str) -> Session:
        data = self._request(
            "POST", "/v1/sessions/switch-org", {"organization_id": organization_id}
        )
        return Session(**_keep(data, Session))

    # ------------------------------------------------------------------
    # internal
    # ------------------------------------------------------------------

    def _request(self, method: str, path: str, body: dict[str, Any] | None = None) -> Any:
        headers = {
            "authorization": f"Bearer {self.api_key}",
            "user-agent": "authio-python/0.1.0",
        }
        resp = self._http.request(
            method, self.base_url + path, headers=headers, json=body
        )
        if resp.status_code >= 400:
            try:
                err = resp.json()
            except ValueError:
                err = {}
            raise AuthioError(
                code=err.get("code", "request_failed"),
                message=err.get("message", resp.reason_phrase),
                status=resp.status_code,
                request_id=err.get("request_id"),
            )
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()


def _seg(value: str) -> str:
    """Percent-encode a caller-supplied ID for use as one URL path segment."""
    return quote(str(value), safe="")


def _keep(raw: dict[str, Any], cls: type) -> dict[str, Any]:
    """Filter ``raw`` to keys understood by the dataclass.

    The API may grow new fields; we ignore unknown ones to avoid version-lock.
    """
    fields = {f for f in cls.__dataclass_fields__}  # type: ignore[attr-defined]
    return {k: v for k, v in raw.items() if k in fields}


__all__ = ["Authio", "AuthioError", "asdict"]
