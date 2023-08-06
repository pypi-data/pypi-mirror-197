from pyxk.lazy_loader import LazyLoader

os = LazyLoader("os", globals())
asyncio = LazyLoader("asyncio", globals())

aiohttp = LazyLoader("aiohttp", globals())
aiofiles = LazyLoader("aiofiles", globals())
progress = LazyLoader("progress", globals(), "rich.progress")

aes = LazyLoader("aes", globals(), "pyxk.aes")
utils = LazyLoader("utils", globals(), "pyxk.utils")


class _AsyncDownload:

    default_timeout = 2 * 60

    def __init__(self, store, limit=8):

        self.store = os.path.join(store, "segments")
        self.limit = limit
        self._temp = store
        self.progress = None
        self.progress_task = None


    def start(self, segments=None, m3u8_keys=None):
        """开启异步下载"""
        if not segments:
            return None

        cipher = {index: aes.Cryptor(**key["cipher"]) for index, key in m3u8_keys.items()}
        os.makedirs(self.store, exist_ok=True)

        with progress.Progress(
            *(
                progress.SpinnerColumn("line"),
                progress.TextColumn("[progress.description]{task.completed}/{task.total}"),
                progress.BarColumn(finished_style="green"),
                progress.TaskProgressColumn("[progress.percentage]{task.percentage:>6.2f}%"),
                progress.TimeElapsedColumn()
            ),
        ) as self.progress:
            self.progress_task = self.progress.add_task(description=None, total=len(segments))
            result = asyncio.run(self.download_manager(segments=segments, cipher=cipher))
        return result


    async def download_manager(self, segments, cipher=None):
        """异步下载管理器"""
        timeout   = aiohttp.ClientTimeout(total=self.default_timeout)
        connector = aiohttp.TCPConnector(limit=self.limit)
        headers   = utils.default_headers()

        async with aiohttp.ClientSession(
            timeout=timeout, connector=connector, headers=headers
        ) as session:
            tasks = [
                self.request(
                    session=session,
                    segment=segment,
                    file=index,
                    cipher=cipher,
                )
                for index, segment in segments.items() # if index < 109
            ]
            result = await asyncio.gather(*tasks)
        return result


    async def request(
        self, session, segment, file, cipher=None
    ):
        """单次异步请求"""
        file = os.path.join(self.store, f"{file}.ts")
        if not os.path.isfile(file) or os.path.getsize(file) == 0:
            content = await self._request(session=session, uri=segment["uri"])
            # 解密 segments
            if cipher and segment["key"] is not None:
                content = cipher[segment["key"]].decrypt(content)
            # 保存 segment
            async with aiofiles.open(file, "wb") as fileobj:
                await fileobj.write(content)

        self.progress.update(self.progress_task, advance=1)
        return file


    @staticmethod
    async def _request(session, uri):
        """获取segment内容"""
        while True:
            try:
                async with session.get(url=uri) as response:
                    # 异常状态码捕获
                    if 403 <= response.status <= 410:
                        raise aiohttp.InvalidURL(
                            f"invalid url:{str(response.url)!r}, status_code: {response.status!r}"
                        )
                    # 重试部分请求
                    if response.status != 200:
                        await asyncio.sleep(1)
                        continue

                    content = await response.content.read()
                    return content
            # 请求超时 重试
            except asyncio.exceptions.TimeoutError:
                await asyncio.sleep(1)
            # 连接错误 重试
            except (
                aiohttp.client_exceptions.ClientOSError,
                aiohttp.client_exceptions.ClientPayloadError,
                aiohttp.client_exceptions.ClientConnectorError,
            ):
                await asyncio.sleep(2)
            # 服务器拒绝连接
            except aiohttp.client_exceptions.ServerDisconnectedError:
                await asyncio.sleep(2)
