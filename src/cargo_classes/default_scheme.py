from cargo_classes import CargoClassSchemes


def main():
    # just a simple wrapper to get the default cargo class scheme in an easier module import
    # note that we support rendering multiple schemes in the docs, to support comparing changes
    cargo_class_schemes = CargoClassSchemes()
    return cargo_class_schemes.default_scheme


if __name__ == "__main__":
    main()
