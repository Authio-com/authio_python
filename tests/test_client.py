import pytest

from authio import Authio, AuthioError, User


def test_requires_api_key():
    with pytest.raises(ValueError):
        Authio(api_key="")


def test_construct_with_base_url():
    c = Authio(api_key="sk_test_x", base_url="https://api.example/")
    assert c.base_url == "https://api.example"


def test_authio_error_carries_metadata():
    e = AuthioError(code="x", message="m", status=418, request_id="r1")
    assert e.code == "x"
    assert e.status == 418
    assert e.request_id == "r1"


def test_user_dataclass():
    u = User(
        id="user_1",
        project_id="proj_1",
        email="a@b.c",
        email_verified=True,
    )
    assert u.email == "a@b.c"


def test_path_ids_are_escaped():
    import httpx

    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request.url.raw_path.decode())
        return httpx.Response(200, json={})

    c = Authio(api_key="sk_test_x", client=httpx.Client(transport=httpx.MockTransport(handler)))
    evil = "../../admin?x=1#"
    try:
        c.get_user(evil)
    except Exception:
        pass
    try:
        c.list_memberships(evil)
    except Exception:
        pass
    c.remove_member("o/1", "m/../2")
    assert seen == [
        "/v1/users/..%2F..%2Fadmin%3Fx%3D1%23",
        "/v1/users/..%2F..%2Fadmin%3Fx%3D1%23/memberships",
        "/v1/organizations/o%2F1/memberships/m%2F..%2F2",
    ]
