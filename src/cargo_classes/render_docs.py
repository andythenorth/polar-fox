from cargo_classes import CargoClassManager

# just a simple wrapper to render the docs on demand
# note that we intentionally include the rendered docs in the repo,
# that isn't always good practice for generated assets
# but I want the rendered html publicly available on github if the docs site disappears for any reason


def main():
    print("[CARGO CLASSES - RENDER DOCS]")
    cargo_class_manager = CargoClassManager()
    cargo_class_manager.render_docs()
    print("[CARGO CLASSES - RENDER DOCS] - complete")


if __name__ == "__main__":
    main()
