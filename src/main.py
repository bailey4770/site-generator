import os
import pathlib
import shutil

PUBLIC_PATH = "./public"
STATIC_PATH = "./static"


def fill_public():
    def _copy_recursive(curr_dir: str):
        contents = os.listdir(curr_dir)

        for elem in contents:
            curr_elem = os.path.join(curr_dir, elem)
            if not os.path.isfile(curr_elem):
                _copy_recursive(curr_elem)
                continue

            # replace static element of path with public
            dst = pathlib.Path(PUBLIC_PATH).joinpath(*pathlib.Path(curr_elem).parts[2:])
            dst.parent.mkdir(parents=True, exist_ok=True)  # Create missing directories
            copied = shutil.copyfile(curr_elem, dst)
            print(copied)

    if not os.path.exists(PUBLIC_PATH):
        os.mkdir(PUBLIC_PATH)

    _copy_recursive(STATIC_PATH)


def main():
    fill_public()


if __name__ == "__main__":
    main()
