import os
import tomllib
from chameleon import PageTemplateLoader


def print_toml(data, indent=0):
    for key, value in data.items():
        if isinstance(value, dict):
            print("    " * indent + f"{key}:")
            print_toml(value, indent + 1)
        elif isinstance(value, list):
            print("    " * indent + f"{key}: [")
            for item in value:
                if isinstance(item, dict):
                    print("    " * (indent + 1) + "{")
                    print_toml(item, indent + 2)
                    print("    " * (indent + 1) + "},")
                else:
                    print("    " * (indent + 1) + f"{item},")
            print("    " * indent + "]")
        else:
            print("    " * indent + f"{key}: {value}")


def render_html_docs(cargo_classes_taxonomy, cargo_classes_dir):
    docs_template = PageTemplateLoader(cargo_classes_dir, format="text")[
        "cargo_classes.pt"
    ]

    rendered_html = docs_template(cargo_classes_taxonomy=cargo_classes_taxonomy)

    dist_dir = os.path.join(cargo_classes_dir, "dist")
    os.makedirs(dist_dir, exist_ok=True)
    output_file_path = os.path.join(dist_dir, "cargo_classes.html")
    with open(output_file_path, "w", encoding="utf-8") as html_file:
        html_file.write(rendered_html)


def main():
    current_dir = os.curdir
    cargo_classes_dir = os.path.join(current_dir, "src", "cargo_classes")
    toml_file_path = os.path.join(cargo_classes_dir, "cargo_classes.toml")

    with open(toml_file_path, "rb") as toml_file:
        cargo_classes_taxonomy = tomllib.load(toml_file)

    print("Parsed TOML Configuration:")
    print_toml(cargo_classes_taxonomy)

    render_html_docs(cargo_classes_taxonomy, cargo_classes_dir)


if __name__ == "__main__":
    main()
