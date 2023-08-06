from dataclasses import dataclass
from typing import Optional

import requests
from requests.auth import HTTPBasicAuth


@dataclass
class Login:
    username: str
    password: str


@dataclass
class API:
    _url_prefix: str
    _auth_token: Optional[str] = None

    def _put_extra_headers(self, kwargs):
        extra_headers = kwargs.get("headers")
        if self._auth_token:
            if extra_headers is None:
                extra_headers = {}
                kwargs["headers"] = extra_headers
            extra_headers["Authorization"] = f"Bearer {self._auth_token}"
    def http_get(self, path, **kwargs):
        url = self._url_prefix + path
        self._put_extra_headers(kwargs)
        return http_get(url, **kwargs, )

    def http_put(self, path, **kwargs):
        url = self._url_prefix + path
        self._put_extra_headers(kwargs)
        return http_put(url, **kwargs)


    def http_patch(self, path, **kwargs):
        url = self._url_prefix + path
        self._put_extra_headers(kwargs)
        return http_patch(url, **kwargs)

    def http_post(self, path, **kwargs):
        url = self._url_prefix + path
        self._put_extra_headers(kwargs)
        return http_post(url, **kwargs)

    def http_delete(self, path, **kwargs):
        url = self._url_prefix + path
        self._put_extra_headers(kwargs)
        return http_delete(url, **kwargs)


def _default_resp_checker(resp):
    status = resp.status_code
    url = resp.url
    if status >= 300:
        raise Exception(f"{status=} {url=}")
    return True


def http_get(path, **kwargs):
    return http_request("get", path=path, **kwargs)


def http_put(path, **kwargs):
    return http_request("put", path=path, **kwargs)


def http_patch(path, **kwargs):
    return http_request("patch", path=path ** kwargs)


def http_post(path, **kwargs):
    return http_request("post", path=path, **kwargs)


def http_delete(path, **kwargs):
    return http_request("delete", path=path, **kwargs)


def http_request(
        method: str,
        path: str,
        json=None,
        data=None,
        login=None,
        params=None,
        headers=None,
        status_checker=_default_resp_checker,
        **kwargs
):
    auth = HTTPBasicAuth(login.username, login.password) if login else None
    resp = requests.request(method, path, auth=auth, json=json, data=data, params=params, headers=headers, **kwargs)
    if status_checker is not None:
        status_checker(resp)
    return resp
