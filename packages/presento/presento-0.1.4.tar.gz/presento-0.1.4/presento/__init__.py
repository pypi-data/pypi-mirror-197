import importlib.resources as pkg_resources
import tempfile
import zipfile
from pathlib import Path
from shutil import move
from subprocess import Popen
from textwrap import dedent
from time import sleep
from webbrowser import open as browser_open
from typing import Optional
from markdown import markdown

import presento

REVEAL_ZIP_FILE = "reveal.js-master.zip"


class Presentation:
    def __init__(self) -> None:
        self.slides: list[str] = []
        self.cdn_js: list[str] = []

    def add_md_slide(self, content: str) -> None:
        self.slides.append(markdown(dedent(content)))

    def add_html_slide(self, content: str) -> None:
        self.slides.append(content)

    def slides_html(self) -> str:
        return "\n".join(f"<section>{s}</section>" for s in self.slides)

    def cdn_imports_html(self) -> str:
        return "\n".join(f'<script src="{s}"></script>' for s in self.cdn_js)

    def add_cdn_js(self, url: str) -> None:
        self.cdn_js.append(url)

    def save_folder(self, folder: Optional[Path]) -> None:
        if isinstance(folder, str):
            folder = Path(folder)
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmpdirpath = Path(tmpdirname)
            with zipfile.ZipFile(
                pkg_resources.open_binary(presento, REVEAL_ZIP_FILE), "r"
            ) as zip_ref:
                zip_ref.extractall(tmpdirname)
            move(tmpdirpath / REVEAL_ZIP_FILE.replace(".zip", ""), folder)
        with open(folder / "index.html", "r+") as frw:
            slides_file = frw.read()
            slides_file = slides_file.replace("<section>Slide 2</section>", "")
            slides_file = slides_file.replace(
                "<section>Slide 1</section>", self.slides_html()
            )
            slides_file = slides_file.replace(
                "<title>reveal.js</title>", self.cdn_imports_html()
            )
            frw.seek(0)
            frw.write(slides_file)

    def show(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmpdirname += "_slides"
            self.save_folder(tmpdirname)
            proc = Popen(f"python3 -m http.server -d {tmpdirname}", shell=True)
            sleep(2)
            browser_open("http://localhost:8000")
