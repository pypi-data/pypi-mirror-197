# Browse pyscript virtual filesystem
from __future__ import annotations

from pathlib import Path
from typing import TypeVar

from pyodide.ffi import create_proxy

HTMLElement = TypeVar('HTMLElement')
from pynanto.remote.widget import Widget


class FilesystemTreeWidget(Widget):
    def __init__(self, path: Path = Path('/'), indent=1):
        self._indent = indent
        super().__init__(  # language=HTML
            f"""
            <span id="_entity"></span>
            <span id="_download">&nbsp ↓ &nbsp</span>
            <div id="_children" style="margin-left: 1em"></div>
            
            """
        )
        self.path = Path(path)
        self._entity: HTMLElement = self
        self._children: HTMLElement = self
        self._download: HTMLElement = self

    def after_render(self):

        self._entity.onclick = create_proxy(self.toggle_display)
        self._download.onclick = create_proxy(self.download)

        # if not self.is_dir():
        #     self._download.style.display = 'none'

        if self._indent > 1:
            self.toggle_display()

        self._update_caption()

        if self.is_dir():
            self._recurse()

    def is_dir(self):
        # return self.path.is_dir() # in pyodide: `PermissionError: [Errno 63] Operation not permitted: '/proc/self/fd'`
        return os.path.isdir(self.path)

    def toggle_display(self, *args):
        self._children.style.display = '' if self._children_hidden() else 'none'
        self._update_caption()

    def download(self, *args):
        console.log(f'click {self.path.absolute()}')
        if self.is_dir():
            download_file(self.path.name + '.zip', zip_in_memory(self.path))
        else:
            download_file(self.path.name, self.path.read_bytes())

    def _update_caption(self):
        if_dir = '▸' if self._children_hidden() else '▼'
        pre = if_dir if self.is_dir() else ' '
        self._entity.innerHTML = (f'<span style="display:inline-block; width: 1em">{pre}</span>'
                                  + ' ' + self.path.name)

    def _children_hidden(self):
        s = self._children.style
        return not s.display == ''

    def _recurse(self):
        for child in self.path.glob('*'):
            w = FilesystemTreeWidget(child, self._indent + 1)
            w.append_to(self._children)


import base64
import mimetypes

from js import document, console


def download_file(filename: str, content: bytes, mime_type: str = None):
    if mime_type is None:
        gt = mimetypes.guess_type(filename)
        mime_type = gt[0]
        if mime_type is None:
            mime_type = 'application/octet-stream'
        console.log(f'guess mime type for `{filename}` is `{mime_type}`')
    a = document.createElement('a')
    a.download = filename
    a.href = f'data:{mime_type};base64,{base64.b64encode(content).decode("ascii")}'
    document.body.append(a)
    a.click()


import os
import zipfile
from io import BytesIO


def _zip_path(zip_file, path):
    path = str(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            zip_file.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file),
                                           os.path.join(path, '..')))


def zip_in_memory(path):
    stream = BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1) as zip_file:
        _zip_path(zip_file, path)

    stream.seek(0)
    return stream.getbuffer().tobytes()
