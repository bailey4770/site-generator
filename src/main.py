import os
from pathlib import Path
import shutil

import config as cfg
from md_converter import md_to_html_node


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
            print(f"copied {curr_elem} to {copied}")

    if not os.path.exists(public_path):
        os.mkdir(public_path)
    else:
        _delete_recursive(public_path)
        print("cleared", public_path)

    _copy_recursive(static_path)


def extract_title(markdown: str):
    for line in markdown.splitlines():
        parts = line.split()

        if not parts:
            continue
        if parts[0] == "#":
            return " ".join(parts[1:])

    raise ValueError("no title found in markdown")


def generate_page(src: Path, template_path: Path, dst: Path):
    print(f"Generating page from {src} to {dst} using template {template_path}")

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
    generate_page(content_path.joinpath("index.md"), template_path, public_path)


if __name__ == "__main__":
    main()
