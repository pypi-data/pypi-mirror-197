import importlib.resources as pkg_resources
import tempfile
import zipfile
from os import system
from pathlib import Path
from shutil import move
from subprocess import Popen
from textwrap import dedent
from time import sleep
from typing import Optional, Union
from webbrowser import open as browser_open

import presento

REVEAL_ZIP_FILE = "reveal.js-master.zip"


class Presentation:
    def __init__(
        self,
        theme: str = "black",
        extra_style: str = "",
    ) -> None:
        self.slides: list[str] = []
        self.cdn_js: list[str] = []
        self.theme = theme
        self.extra_style = extra_style

    def add_md_slide(self, content: str, extra_style: str = "") -> None:
        self.slides.append(
            f'<section data-markdown style="{extra_style}"><textarea data-template>{dedent(content)}</textarea></section>'
        )

    def add_html_slide(self, content: str) -> None:
        self.slides.append(f"<section>{content}</section>")

    def slides_html(self) -> str:
        return "\n".join(self.slides)

    def cdn_imports_html(self) -> str:
        return "\n".join(f'<script src="{s}"></script>' for s in self.cdn_js)

    def add_cdn_js(self, url: str) -> None:
        self.cdn_js.append(url)

    def add_columns_slide(
        self,
        columns_html: list[str],
        grid_gap: str = "1%",
        column_sizes: Optional[str] = None,
        title: str = "",
    ) -> None:
        if column_sizes is None:
            column_sizes = " ".join(
                f"{int(100 / len(columns_html) - len(columns_html))}%"
                for _ in columns_html
            )

        grid_snippet = dedent(
            f"""
            <section><h2 class="r-fit-text">{title}</h2>
        <div style="display: grid; grid-template-columns: {column_sizes}; grid-gap: {grid_gap};">
        """
        )
        grid_snippet += "\n".join(f"<div>{ch}</div>" for ch in columns_html)
        grid_snippet += "</div></section>"
        self.slides.append(grid_snippet)

    def save_folder(self, folder: Union[Path, str]) -> None:
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
            slides_file = slides_file.replace(
                "dist/theme/black.css", f"dist/theme/{self.theme}.css"
            )
            slides_file = slides_file.replace(
                "</head>", f"""<style>{self.extra_style}</style></head>"""
            )
            frw.seek(0)
            frw.write(slides_file)

    def show(self, port: int = 9000) -> None:
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmpdirname += "_slides"
            self.save_folder(tmpdirname)
            command = f"python3 -m http.server -d {tmpdirname} {port}"
            # ugly but effective trick:
            # start a server in background
            proc = Popen(command, shell=True)
            # wait a bit for it to be up, basically does nothing but listen to the port
            sleep(1)
            # now open the browser on that page
            browser_open(f"http://localhost:{port}")
            # wait a bit so the browser can load the assets
            sleep(3)
            # now kill it and run the server as a foreground process
            # that will be terminated with the script itself without dangling processes
            proc.kill()
            system(command)
