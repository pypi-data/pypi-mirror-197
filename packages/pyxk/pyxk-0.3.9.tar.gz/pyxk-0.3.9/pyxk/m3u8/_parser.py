from pyxk.lazy_loader import LazyLoader
from pyxk.m3u8._download import _AsyncDownload

os = LazyLoader("os", globals())
shlex = LazyLoader("shlex", globals())
warnings = LazyLoader("warnings", globals())
threading = LazyLoader("threading", globals())
subprocess = LazyLoader("subprocess", globals())

rich = LazyLoader("rich", globals())
_m3u8 = LazyLoader("_m3u8", globals(), "m3u8")
panel = LazyLoader("panel", globals(), "rich.panel")
columns = LazyLoader("columns", globals(), "rich.columns")
progress = LazyLoader("progress", globals(), "rich.progress")

utils = LazyLoader("utils", globals(), "pyxk.utils")
requests = LazyLoader("requests", globals(), "pyxk.requests")



class M3U8():
    """m3u8 下载器"""

    default_limit = 8
    default_filename = "index.mp4"

    def __init__(self):

        self._headers = {}
        self._verify  = True
        self._file = None
        self._temp = None
        self._limit = self.default_limit
        self._rerequest = False
        self._reserve_segments = False
        self._delete_m3u8file = False
        self._session = requests.Session()


    def _get_m3u8_content(self, uri, file, encoding="UTF-8", *, m3u8key=False):
        """获取 m3u8 文件内容"""
        file = os.path.join(self._temp, utils.hash256(file))
        file = file + ".key" if m3u8key else file + ".m3u8"

        if self._rerequest or not os.path.isfile(file):
            response = self._session.get(url=uri, headers=self._headers, verify=self._verify)
            return getattr(response, "content") if m3u8key else getattr(response, "text")

        mode, encoding = "rb" if m3u8key else "r", None if m3u8key else encoding
        with open(file, mode, encoding=encoding) as fileobj:
            content = fileobj.read()
        return content


    def _sava_m3u8_content(self, file, content, encoding="UTF-8", *, m3u8key=False):
        """保存 m3u8 文件内容"""
        if not isinstance(file, str) or not file:
            return
        file = os.path.join(self._temp, utils.hash256(file))
        file = file + ".key" if m3u8key else file + ".m3u8"

        if self._rerequest or not os.path.isfile(file):
            mode, encoding = "wb" if m3u8key else "w", None if m3u8key else encoding
            with utils.open(file, mode, encoding=encoding) as fileobj:
                fileobj.write(content)


    def _file_abspath(self, file, /):
        """文件绝对路径"""
        if not isinstance(file, str) or not file:
            file = self.default_filename
        file = "-".join(os.path.normpath(os.path.abspath(file)).strip().split())
        file = utils.rename_file(file, suffix="mp4")
        self._file = file[0]
        self._temp = os.path.join(file[1], file[2].removesuffix("mp4") + "temp")


    def _initialization(
        self, file=None, headers=None, verify=True, rerequest=False, delete=False, reserve=False, limit=8
    ):
        self._file_abspath(file)
        self._headers = dict(headers) if headers else {}
        self._verify = bool(verify)
        self._rerequest = bool(rerequest)
        self._delete_m3u8file = bool(delete)
        self._reserve_segments = bool(reserve)
        if not isinstance(limit, int) or limit <= 0:
            limit = self.default_limit
        self._limit = limit


    def load(
        self, uri, **kwargs
    ):
        """解析 m3u8 链接"""
        self._initialization(**kwargs)
        content = self._get_m3u8_content(uri=uri, file=uri)
        return self._start(content=content, uri=uri)


    def loads(
        self, content, uri=None, **kwargs
    ):
        """解析 m3u8 链接"""
        self._initialization(**kwargs)
        if content.startswith("#EXTM3U"):
            return self._start(content=content, uri=uri)

        _m3u8file = os.path.normpath(os.path.abspath(content))
        if os.path.isfile(_m3u8file):
            with open(_m3u8file, "r", encoding="utf-8") as fileobj:
                content = fileobj.read()
        return self._start(content=content, uri=uri)


    def _start(self, content, uri=None):
        """解析 m3u8 入口"""
        # playlists
        m3u8_obj, variant_uri = self._parse_playlist(
            m3u8_obj=_m3u8.loads(content=content, uri=uri), uri=uri
        )
        # m3u8 keys
        m3u8_keys = self._parse_m3u8_keys(m3u8_obj=m3u8_obj)
        # segments
        segments, duration = self._parse_segments(
            m3u8_obj=m3u8_obj, uri=variant_uri, m3u8_keys=m3u8_keys
        )
        self._display(uri=uri, maximum=len(segments), duration=duration, encryption=bool(m3u8_keys))

        # 异步下载
        download = _AsyncDownload(store=self._temp)
        download_result = download.start(segments=segments, m3u8_keys=m3u8_keys)

        # 合并 segments
        merge_result = self._merge_segments(files=download_result)
        # 删除 segments
        if merge_result and not self._reserve_segments:
            for segment in download_result:
                os.remove(segment)
            if not os.listdir(download.store):
                os.rmdir(download.store)
        # 删除 m3u8 文件
        if self._delete_m3u8file and os.path.isdir(self._temp):
            for file in os.listdir(self._temp):
                file = os.path.join(self._temp, file)
                if not os.path.isfile(file):
                    continue
                os.remove(file)
            if not os.listdir(self._temp):
                os.rmdir(self._temp)


    def _merge_segments(self, files):
        if not files:
            return False

        # 生成filelists文件
        filelists, filesize = os.path.join(self._temp, "filelist.txt"), 0
        with utils.open(filelists, "w", encoding="utf-8") as fileobj:
            for file in files:
                fileobj.write(f"file '{file}'\n")
                filesize += os.path.getsize(file) - 16400

        # ffmpeg合并代码
        merge_code = shlex.split(
            f"ffmpeg -loglevel quiet -f concat -safe 0 -i {filelists} -c copy {self._file} -y"
        )
        merge_complete = False

        # 合并函数
        def merge():
            try:
                subprocess.run(args=merge_code, check=True)
                os.remove(filelists)
            except FileNotFoundError as error:
                reason = getattr(error, "filename", None)
                if reason != "ffmpeg":
                    raise
                warnings.warn("没有ffmpeg, 调用失败")
            finally:
                nonlocal merge_complete
                merge_complete = True

        # 合并进度条函数
        def merge_progress():
            last_filesize = 0
            get_filesize = lambda file: os.path.getsize(file) if os.path.isfile(file) else 0
            # 进度条
            with progress.Progress(
                *(
                    progress.SpinnerColumn("line"),
                    progress.DownloadColumn(),
                    progress.BarColumn(finished_style="green"),
                    progress.TaskProgressColumn("[progress.percentage]{task.percentage:>6.2f}%"),
                    progress.TimeElapsedColumn()
                ),
                transient=True
            ) as progressing:

                progress_task = progressing.add_task(description=None,total=filesize)
                while True:
                    current_filesize = get_filesize(self._file)
                    progressing.update(progress_task, advance=current_filesize-last_filesize)
                    last_filesize = current_filesize
                    # 控制进度条退出
                    if merge_complete:
                        progressing.update(progress_task, advance=abs(filesize-last_filesize))
                        break

        task1 = threading.Thread(target=merge)
        task2 = threading.Thread(target=merge_progress)
        task1.start()
        task2.start()
        task1.join()
        task2.join()
        return os.path.isfile(self._file)


    def _parse_playlist(self, m3u8_obj, uri=None):
        if not m3u8_obj.is_variant:
            return m3u8_obj, uri

        def sort_playlist(playlist):
            playlist.uri = playlist.absolute_uri
            return playlist.stream_info.bandwidth
        playlists = sorted(m3u8_obj.playlists, key=sort_playlist)

        # 保存playlists
        self._sava_m3u8_content(file=uri, content=m3u8_obj.dumps())

        variant_uri = playlists[-1].uri
        content = self._get_m3u8_content(uri=variant_uri, file=variant_uri)

        return self._parse_playlist(
            m3u8_obj=_m3u8.loads(
                content=content, uri=variant_uri
            ),
            uri=variant_uri
        )


    def _parse_m3u8_keys(self, m3u8_obj):
        m3u8_keys = {}
        for index, key in enumerate(m3u8_obj.keys):
            if not key:
                continue
            key.uri = key.absolute_uri
            secret  = self._get_m3u8_content(uri=key.uri, file=key.uri, m3u8key=True)
            # 保存密钥
            self._sava_m3u8_content(file=key.uri, content=secret, m3u8key=True)
            m3u8_keys[index] = {
                "cipher": {
                    "key": secret,
                    "iv": key.iv.removeprefix("0x")[:16] if key.iv else secret[:16]
                },
                "uri": key.uri,
                "method": key.method
            }
        return m3u8_keys


    def _parse_segments(self, m3u8_obj, uri=None, m3u8_keys=None):
        segments, duration = {}, 0
        for index, segment in enumerate(m3u8_obj.segments):
            segment.uri, key_flags = segment.absolute_uri, None
            if segment.key and m3u8_keys:
                for key, val in m3u8_keys.items():
                    if segment.key.method == val["method"] and segment.key.uri == val["uri"]:
                        key_flags = key
                        break
            segments[index] = {"uri": segment.uri, "key": key_flags}
            duration += segment.duration

        if m3u8_obj.is_endlist:
            self._sava_m3u8_content(file=uri, content=m3u8_obj.dumps())
        return segments, duration


    def _display(self, uri, maximum, duration, encryption):
        visual_data = [
            f"Limit: {self._limit}",
            f"Maximum: {maximum}",
            f"PlayTime: {utils.human_playtime_pr(duration)}",
            f"Encryption: {encryption}",
            f"FileName: [magenta]{os.path.basename(self._file)}[/]",
            f"FilePath: {os.path.dirname(self._file)}"
        ]
        visual_data = [f"{i+1} {x}" for i, x in enumerate(visual_data)]
        if uri:
            visual_uri = panel.Panel(columns.Columns([uri], expand=True, align="center"))
            visual_data.insert(0, visual_uri)
        visual_data.append(
            "[green b]Parsing success ![/]" if maximum \
            else "[red b]Parsing failure ![/]"
        )
        visual_data = columns.Columns(visual_data, expand=True,)
        visual_data = panel.Panel(visual_data, border_style="yellow")
        rich.print(visual_data)
