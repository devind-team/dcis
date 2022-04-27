import os
from os import path
from pathlib import Path


def init() -> None:
    root = Path(__file__).resolve(strict=True).parent
    server_storage = path.join(root, 'server', 'storage')
    client_storage = path.join(root, 'client', 'static', 'storage')
    os.symlink(server_storage, client_storage)


if __name__ == '__main__':
    init()
