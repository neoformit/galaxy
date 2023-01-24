"""Manage extraction of archives.

For URL fetch, download is streamed to extract specified files from archive. 
"""

import contextlib
import os
import tarfile
from http.client import HTTPSConnection

HTTPS_PORT = 443


def fetch_tar(host: str, path: str, targets: list=[], compression: str='gz'):
    """Download and unpack tar file on-the-fly and call item_handler for each entry.

    The ``item_handler`` function will receive the arguments TarFile (the currently extracted stream),
    the current TarInfo object and a list of target paths to extract, which should be either a path
    to a file or a directory (ending in '/').
    """
    items_found = 0
    with contextlib.closing(HTTPSConnection(host=host, port=HTTPS_PORT)) as client:
        client.request('GET', path)
        with client.getresponse() as r:
            code = r.getcode()
            if code < 200 or code >= 300:
                raise Exception(f'HTTP error downloading tar: code: {code}')
            try:
                with tarfile.open(fileobj=r, mode=f'r|{compression}') as tar:
                    for tarinfo in tar:
                        items_found += save_target(tar, tarinfo, targets)
            except Exception as e:
                raise Exception(f'Failed to extract tar stream: {e}')


def save_target(tar: tarfile.TarFile, tarinfo: tarfile.TarInfo, targets: list[str]):
    if [t for t in targets if tarinfo.name.startswith(t)]:
        if not tarinfo.isdir():
            path = os.path.join('/home/cameron/Downloads/stream-archive', tarinfo.name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            print("Extracting file to", path)
            with tar.extractfile(tarinfo) as f:
                with open(path, 'wb') as w:
                    w.write(f.read())
            return 1
    return 0


if __name__ == '__main__':
    # Test download
    url = 'dl.discordapp.net'
    path = '/apps/linux/0.0.15/discord-0.0.15.tar.gz'
    targets = ['Discord/resources/']
    fetch_tar(
        url,
        path,
        targets=targets,
    )
