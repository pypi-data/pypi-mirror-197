import ast
import click
from pyxk.m3u8._parser import M3U8


@click.command()
@click.argument("uri", metavar="m3u8链接地址", type=str)
@click.option("-o", "--output", help="下载保存文件名称", default=None, type=str)
@click.option("-r", "--rerequest/--no-rerequest", help="重新请求m3u8资源", default=False)
@click.option("--delete/--no-delete", help="下载完成后, 删除m3u8本地资源", default=True)
@click.option("--reserve/--no-reserve", help="下载完成后, 保留segments", default=False)
@click.option("--headers", help="request请求头", default=None, type=str)
@click.option("--verify/--no-verify", help="request SSL验证", default=True)
@click.option("--limit", help="异步下载limit", default=8, type=int)
def main(
    uri, output, rerequest, delete, reserve, headers, verify, limit
):
    m3u8parse_params = {
        "file": output,
        "headers": headers,
        "verify": verify,
        "rerequest": rerequest,
        "delete": delete,
        "reserve": reserve,
        "limit": limit,
    }
    m3u8_obj = M3U8()
    m3u8_obj.load(uri=uri, **m3u8parse_params)
