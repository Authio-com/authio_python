<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/logo-dark.png">
    <img alt="Authio" src=".github/logo-light.png" width="220">
  </picture>
</p>

# authio (Python)

Authio Python server SDK. Multi-org-first auth for B2B Python apps (FastAPI, Django, Flask, Litestar, etc.).

## What's new — 2026-05-23 WorkOS-parity sprint

Four new product surfaces shipped on the Authio API
([`authio_proto`](https://github.com/authio-com/authio_proto)). Python idiomatic bindings for all four are on the next-release roadmap;
Flask snippets for the HMAC verifier are already published on the docs:

- **Embeddable widgets** — drop-in React surface; mint widget tokens
  from any Python BFF via `POST /v1/widget-tokens`. See
  [docs.authio.com/widgets/overview](https://docs.authio.com/widgets/overview).
- **Synchronous Actions** — customer-hosted HTTPS webhook with
  HMAC-SHA256 envelope. Python (Flask) signature verification on
  [docs.authio.com/actions/signature-verification](https://docs.authio.com/actions/signature-verification).
- **Dynamic Client Registration + CIMD** — RFC 7591 / 7592 +
  MCP-spec 2025-11-25 preferred path. See
  [docs.authio.com/guides/mcp-integration](https://docs.authio.com/guides/mcp-integration).
- **Roles + permissions on the JWT** — the existing
  `verify_session()` path now exposes `claims["roles"]` (str in
  single-role mode, list in multi-role) and `claims["permissions"]`
  (always list). See
  [docs.authio.com/concepts/roles-and-permissions](https://docs.authio.com/concepts/roles-and-permissions).

## Install

```bash
pip install authio
```

## Quick start

```python
from authio import Authio

client = Authio(api_key="sk_live_...")
memberships = client.list_memberships("user_01HX...")
```

## License

MIT
