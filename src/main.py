import os
from pathlib import Path
import shutil
import logging

import config as cfg
from md_converter import md_to_html_node


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=cfg.get_logging_level(),
)


def get_static_content(public_path: Path, static_path: Path):
    def _delete_recursive(curr_dir: Path):
        contents = os.listdir(curr_dir)

        for elem in contents:
            curr_elem = curr_dir.joinpath(elem)
            if not os.path.isfile(curr_elem):
                _delete_recursive(curr_elem)
                os.rmdir(curr_elem)
                continue

            os.remove(curr_elem)

    def _copy_recursive(curr_dir: Path):
        contents = os.listdir(curr_dir)

        for elem in contents:
            curr_elem = curr_dir.joinpath(elem)
            if not os.path.isfile(curr_elem):
                _copy_recursive(curr_elem)
                continue

            # replace static element of path with public
            dst = public_path.joinpath(*curr_elem.parts[1:])
            dst.parent.mkdir(parents=True, exist_ok=True)  # Create missing directories

            copied = shutil.copyfile(curr_elem, dst)
            logger.info(f"copied {curr_elem} to {copied}")

    if not os.path.exists(public_path):
        os.mkdir(public_path)
    else:
        _delete_recursive(public_path)
        logger.info("cleared %s", public_path)

    _copy_recursive(static_path)


def get_web_content(public_path: Path, content_path: Path, template_path: Path):
    content = os.listdir(content_path)
    for item in content:
        item_path: Path = content_path.joinpath(item)
        if os.path.isfile(item_path):
            generate_page(item_path, template_path, public_path)
        else:
            new_public_path = public_path.joinpath(item)
            os.mkdir(new_public_path)
            get_web_content(new_public_path, item_path, template_path)


def extract_title(markdown: str):
    for line in markdown.splitlines():
        parts = line.split()

        if not parts:
            continue
        if parts[0] == "#":
            return " ".join(parts[1:])

    raise ValueError("no title found in markdown")


def generate_page(src: Path, template_path: Path, dst: Path):
    logger.info(f"Generating page from {src} to {dst} using template {template_path}")

    with open(src, "r") as f:
        md = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(md)
    content_html = md_to_html_node(md).to_html()

    index_html = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", content_html
    )

    with open(dst.joinpath("index.html"), "w") as f:
        _ = f.write(index_html)


def main():

    public_path, static_path, content_path, template_path = (
        cfg.get_public_path(),
        cfg.get_static_path(),
        cfg.get_content_path(),
        cfg.get_template_path(),
    )

    get_static_content(public_path, static_path)
    get_web_content(public_path, content_path, template_path)
    logger.info("Website generated")


if __name__ == "__main__":
    main()
