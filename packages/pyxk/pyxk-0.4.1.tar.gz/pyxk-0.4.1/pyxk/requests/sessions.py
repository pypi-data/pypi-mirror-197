import requests
from pyxk.lazy_loader import LazyLoader

os = LazyLoader("os", globals())
time = LazyLoader("time", globals())
warnings = LazyLoader("warnings", globals())
urlparse = LazyLoader("urlparse", globals(), "urllib.parse")
utils = LazyLoader("utils", globals(), "pyxk.utils")
console = LazyLoader("console", globals(), "rich.console")
progress = LazyLoader("progress", globals(), "rich.progress")


class Session(requests.Session):
    """requests.Session 重构

    pip install requests
    """

    def __init__(self, *, base_url: str=""):
        super().__init__()
        self.headers["User-Agent"] = utils.UA_ANDROID
        self._base_url = self.__set_base_url(base_url)
        self.__console = console.Console()

    def __set_base_url(self, url, /):
        """配置 base_url"""
        if not isinstance(url, str) or not url:
            return ""
        if not self._is_absolute_url(url):
            raise requests.exceptions.InvalidURL(f"{url!r} 不是绝对路径")
        return url

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, url):
        self._base_url = self.__set_base_url(url)

    @staticmethod
    def _is_absolute_url(url, /):
        url = urlparse.urlsplit(url)
        return bool(url.scheme and url.netloc)

    def _build_absolute_url(self, url, /):
        if self.base_url and not self._is_absolute_url(url):
            return urlparse.urljoin(self.base_url, url)
        return url

    def request(self, method, url, *, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=5, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None):
        url, exc_count, exc_max = self._build_absolute_url(url), {}, 10
        while True:
            try:
                with self.__console.status(f"[magenta b]Send Request[/]: {url}"):
                    response = super().request(method=method, url=url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)
                    break
            except requests.exceptions.Timeout:
                reason = "timeout"
                exc_count.setdefault(reason, 0)
                exc_count[reason] += 1
                if exc_count[reason] >= exc_max:
                    raise
                warnings.warn(f"timeout: {timeout!r}")
                time.sleep(1)
            except requests.exceptions.ConnectionError as exc:
                reason = str(exc.args[0])
                reason_re = ("[Errno 7]", )
                reason_ok = lambda : True in [item in reason for item in reason_re]
                if not reason_ok():
                    raise
                warnings.warn("请检查网络连接是否正常...")
                time.sleep(1)
        return response

    def get(self, url, *, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=5, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None):
        return self.request(method="GET", url=url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)

    def options(self, url, *, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=5, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None):
        return self.request(method="OPTIONS", url=url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)

    def post(self, url, *, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=5, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None):
        return self.request(method="POST", url=url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)

    def delete(self, url, *, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=5, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None):
        return self.request(method="DELETE", url=url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)

    def put(self, url, *, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=5, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None):
        return self.request(method="PUT", url=url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)

    def patch(self, url, *, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=5, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None):
        return self.request(method="PATCH", url=url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)

    def head(self, url, *, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=5, allow_redirects=False, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None):
        return self.request(method="HEAD", url=url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)

    def wget(self, url, method="GET", *, output=None, resume=False, headers=None, stream=True, **kwargs):
        """大文件流式响应下载

        :params: output: 下载文件路径
        :params: resume: 断点续传(default: False)
        """
        output = self.__set_wget_output(url=url, output=output, headers=headers, **kwargs)
        file_size, file_mode, chunk_size = 0, "wb", 1024
        # 开启文件续传
        if resume:
            if not output:
                warnings.warn("文件续传缺少 output")
            elif os.path.isfile(output):
                file_size, file_mode = os.path.getsize(output), "ab"
                headers = requests.structures.CaseInsensitiveDict(dict(headers or {}))
                headers["Range"] = f"bytes={file_size}-"
        response = self.request(method=method, url=url, headers=headers, stream=stream, **kwargs)
        if not output:
            return response
        content_length = response.headers.get("Content-Length")
        if content_length is not None:
            content_length = int(content_length) + file_size
        with progress.Progress(
            *(
                # progress.SpinnerColumn("line"),
                progress.TextColumn("[progress.description]{task.description}"),
                progress.TaskProgressColumn("[progress.percentage]{task.percentage:>6.2f}%"),
                progress.BarColumn(finished_style="green"),
                progress.DownloadColumn(),
                # progress.TransferSpeedColumn(),
                progress.TimeElapsedColumn()
            ),
            console=self.__console, transient=True
        ) as download_progress:
            description = f"[bold]{os.path.basename(output)}[/]"
            download_task = download_progress.add_task(description=description, total=content_length)
            download_progress.update(download_task, advance=file_size)
            with utils.open(file=output, mode=file_mode) as file_obj:
                for chunk in response.iter_content(chunk_size):
                    file_obj.write(chunk)
                    download_progress.update(download_task, advance=chunk_size)
        return response

    def __set_wget_output(self, url, output, headers, **kwargs):

        if not isinstance(output, str):
            return None
        output = os.path.normpath(os.path.abspath(output))
        if len(os.path.basename(output).rsplit(".", 1)) >= 2:
            return output
        head_response = self.head(url=url, headers=headers, **kwargs)
        content_type = head_response.headers.get("Content-Type")
        if not content_type:
            return output
        content_type = content_type.split(";", 1)[0].strip()
        content_type = content_type.rsplit("/", 1)[-1].strip()
        return output + "." + content_type if content_type else output
