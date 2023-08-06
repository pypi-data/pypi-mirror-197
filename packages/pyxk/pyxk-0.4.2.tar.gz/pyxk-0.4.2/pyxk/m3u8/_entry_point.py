import copy
import click
from pyxk.m3u8._m3u8 import load_url, load_content



@click.group(
    invoke_without_command=False,
    chain=True
)
@click.pass_context
@click.option(
    "-o",
    "--output",
    "output",
    type=str,
    default=None,
    help="m3u8 视频保存路径"
)
@click.option(
    "--rerequest",
    is_flag=True,
    default=False,
    help="重新请求 m3u8 网络资源"
)
@click.option(
    "--no-delete",
    "delete",
    is_flag=True,
    default=True,
    help="删除本地 m3u8 文件"
)
@click.option(
    "--reserve",
    "reserve",
    is_flag=True,
    default=False,
    help="保留 segments"
)
@click.option(
    "-h",
    "--headers",
    "headers",
    type=(str, str),
    multiple=True,
    help="Request 请求头"
)
@click.option(
    "--no-verify",
    "verify",
    is_flag=True,
    default=True,
    help="Request SSL验证"
)
@click.option(
    "-l",
    "--limit",
    "limit",
    type=int,
    default=8,
    help="异步下载 Limit"
)
def main(
    ctx, output, rerequest, delete, reserve, headers, verify, limit
):
    """M3U8 下载, 合并管理器(ffmpeg)"""
    ctx.obj = ctx.params


@main.command()
@click.pass_obj
@click.argument(
    "content",
    type=click.Path(exists=True),
    metavar="path: <m3u8 本地文件>"
)
@click.option(
    "-u",
    "--url",
    "url",
    type=str,
    default=None,
    help="m3u8 链接地址"
)
@click.option(
    "-o",
    "--output",
    "output",
    type=str,
    default=None,
    help="m3u8 视频保存路径"
)
def file(obj, content, url, output):
    """使用 m3u8文件 下载"""

    kwargs = copy.deepcopy(obj)
    if output is not None:
        kwargs["output"] = output
    load_content(content=content, url=url, **kwargs)


@main.command()
@click.pass_obj
@click.argument(
    "url",
    type=str,
    metavar="url: <m3u8 链接地址>"
)
@click.option(
    "-o",
    "--output",
    "output",
    type=str,
    default=None,
    help="m3u8 视频保存路径"
)
def url(obj, url, output):
    """使用 m3u8链接 下载"""

    kwargs = copy.deepcopy(obj)
    if output is not None:
        kwargs["output"] = output
    load_url(url=url, **kwargs)
