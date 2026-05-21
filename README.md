<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/logo-dark.png">
    <img alt="Authio" src=".github/logo-light.png" width="220">
  </picture>
</p>

# authio (Python)

Authio Python server SDK. Multi-org-first auth for B2B Python apps (FastAPI, Django, Flask, Litestar, etc.).

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
