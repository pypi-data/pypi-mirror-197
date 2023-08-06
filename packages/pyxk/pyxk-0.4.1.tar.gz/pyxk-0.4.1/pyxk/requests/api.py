from pyxk.requests.sessions import Session


def request(
    method, url, *, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=5, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None
):
    with Session() as session:
        return session.request(
            method=method, url=url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json
        )


def get(
    url, *, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=5, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None
):
    return request(
        method="GET", url=url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json
    )


def post(
    url, *, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=5, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None
):
    return request(
        method="POST", url=url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json
    )


def options(
    url, *, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=5, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None
):
    return request(
        method="OPTIONS", url=url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json
    )


def head(
    url, *, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=5, allow_redirects=False, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None
):
    return request(
        method="HEAD", url=url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json
    )


def put(
    url, *, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=5, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None
):
    return request(
        method="PUT", url=url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json
    )


def patch(
    url, *, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=5, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None
):
    return request(
        method="PATCH", url=url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json
    )


def delete(
    url, *, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=5, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None
):
    return request(
        method="DELETE", url=url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json
    )


def wget(
    url, method="GET", *, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=5, allow_redirects=True, proxies=None, hooks=None, verify=None, cert=None, json=None, stream=True, output=None, resume=False
):
    """大文件流式响应下载

    :params: output: 下载文件路径
    :params: resume: 断点续传(default: False)
    """
    session = Session()
    try:
        response = session.wget(
            method=method, url=url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, verify=verify, cert=cert, json=json, stream=stream, output=output, resume=resume
        )
    finally:
        session.close()
    return response
