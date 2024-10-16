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


def render_html_docs(
    cargo_classes_scheme_name, cargo_classes_config, cargo_classes_dir
):
    docs_template = PageTemplateLoader(cargo_classes_dir, format="text")[
        "cargo_classes.pt"
    ]

    # pop out metadata, the remaining nodes will be the actual classes
    cargo_classes_metadata = cargo_classes_config.pop("METADATA")
    cargo_classes_taxonomy = {
        node: attrs
        for node, attrs in cargo_classes_config.items()
        if "cargo_class_description" in attrs
    }
    example_vehicles = {
        node: attrs
        for node, attrs in cargo_classes_config.items()
        if "vehicle_description" in attrs
    }
    vehicle_cargo_class_mapping = {}
    for cargo_class in cargo_classes_taxonomy:
        example_vehicles_for_cargo_class = []
        for example_vehicle_node_id, example_vehicle_attrs in example_vehicles.items():
            if cargo_class in example_vehicle_attrs["cargo_classes_allowed"]:
                example_vehicles_for_cargo_class.append(example_vehicle_node_id)
        vehicle_cargo_class_mapping[cargo_class] = example_vehicles_for_cargo_class

    rendered_html = docs_template(
        cargo_classes_scheme_name=cargo_classes_scheme_name,
        cargo_classes_metadata=cargo_classes_metadata,
        cargo_classes_taxonomy=cargo_classes_taxonomy,
        example_vehicles=example_vehicles,
        vehicle_cargo_class_mapping=vehicle_cargo_class_mapping,
    )

    dist_dir = os.path.join(cargo_classes_dir, "dist")
    os.makedirs(dist_dir, exist_ok=True)
    output_file_path = os.path.join(dist_dir, cargo_classes_scheme_name + ".html")
    with open(output_file_path, "w", encoding="utf-8") as html_file:
        html_file.write(rendered_html)


def main():
    current_dir = os.curdir
    cargo_classes_dir = os.path.join(current_dir, "src", "cargo_classes")
    for cargo_classes_scheme_name in ["cargo_classes_A"]:
        toml_file_path = os.path.join(
            cargo_classes_dir, cargo_classes_scheme_name + ".toml"
        )

        with open(toml_file_path, "rb") as toml_file:
            cargo_classes_config = tomllib.load(toml_file)

        render_html_docs(
            cargo_classes_scheme_name, cargo_classes_config, cargo_classes_dir
        )


if __name__ == "__main__":
    main()
