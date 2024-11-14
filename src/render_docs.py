from cargo_classes.cargo_classes import CargoClassManager
import shutil
import sys
import os

currentdir = os.curdir


def main():
    print("[RENDER DOCS]")
    docs_src = os.path.join(currentdir, "src", "docs_templates")
    docs_output_path = os.path.join(currentdir, "docs")
    if os.path.exists(docs_output_path):
        shutil.rmtree(docs_output_path)
    os.mkdir(docs_output_path)

    css_dir_src = os.path.join(docs_src, "css")
    css_dir_dst = os.path.join(docs_output_path, "css")
    shutil.copytree(css_dir_src, css_dir_dst)

    shutil.copy(os.path.join(docs_src, "index.html"), docs_output_path)

    cargo_class_manager = CargoClassManager()
    cargo_class_manager.render_docs()
    print("[RENDER DOCS] - complete")


if __name__ == "__main__":
    main()
