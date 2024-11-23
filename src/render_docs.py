import shutil
import sys
import os

currentdir = os.curdir

from chameleon import PageTemplateLoader
from cargo_classes.cargo_classes import CargoClassManager

external_urls = {
    'firs': 'https://grf.farm/firs/latest.html',
    'iron-horse': 'https://grf.farm/iron-horse/latest.html',
}

def render_frax_cargo_class_docs(docs_src, docs_output_path):
    cargo_class_manager = CargoClassManager()
    docs_pages = {
        "industry_frax": "industry_frax.html",
        "frax_overview": "frax.html",
        "vehicle_frax": "vehicle_frax.html",
    }
    for template_name, html_file_name in docs_pages.items():
        docs_template = PageTemplateLoader(docs_src, format="text")[
            template_name + ".pt"
        ]
        rendered_html = docs_template(
            cargo_class_scheme=cargo_class_manager.cargo_class_scheme,
            docs_pages=docs_pages,
            external_urls=external_urls,
        )

        output_file_path = os.path.join(docs_output_path, html_file_name)
        with open(output_file_path, "w", encoding="utf-8") as html_file:
            html_file.write(rendered_html)

def render_general_docs(docs_src, docs_output_path):
    docs_pages = {
        "index": "index.html",
    }
    for template_name, html_file_name in docs_pages.items():
        docs_template = PageTemplateLoader(docs_src, format="text")[
            template_name + ".pt"
        ]
        rendered_html = docs_template(
            docs_pages=docs_pages,
        )

        output_file_path = os.path.join(docs_output_path, html_file_name)
        with open(output_file_path, "w", encoding="utf-8") as html_file:
            html_file.write(rendered_html)

def main():
    print("[RENDER DOCS]")
    docs_src = os.path.join(currentdir, "src", "docs_templates")
    docs_output_path = os.path.join(currentdir, "docs")
    if os.path.exists(docs_output_path):
        shutil.rmtree(docs_output_path)
    os.mkdir(docs_output_path)

    static_dir_src = os.path.join(docs_src, "static")
    static_dir_dst = os.path.join(docs_output_path, "static")
    shutil.copytree(static_dir_src, static_dir_dst)

    shutil.copy(os.path.join(docs_src, "index.html"), docs_output_path)

    render_general_docs(docs_src, docs_output_path)
    render_frax_cargo_class_docs(docs_src, docs_output_path)
    print("[RENDER DOCS] - complete")


if __name__ == "__main__":
    main()
