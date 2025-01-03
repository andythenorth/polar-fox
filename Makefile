# Various needed programs
PYTHON3 = python3

FIND_FILES = bin/find-files

.PHONY: dist cargo_graphics clean install

dist: cargo_graphics cargo_class_nml docs $(shell $(FIND_FILES) --ext=.py --ext=.txt src)
	@ $(PYTHON3) src/build_dist.py

cargo_graphics: $(shell $(FIND_FILES) --ext=.py --ext=.png src)
	@ $(PYTHON3) src/render_cargo_graphics.py

cargo_class_nml: $(shell $(FIND_FILES) --ext=.py --ext=.toml --ext=.pt src/cargo_clases)
	@ $(PYTHON3) src/cargo_classes/render_nml.py

docs: $(shell $(FIND_FILES) --ext=.py --ext=.toml --ext=.pt --ext=.css src)
	@ $(PYTHON3) src/render_docs.py

install: dist
	@ $(PYTHON3) src/install_dist.py

release: docs copy_docs_to_grf_farm

# this expects to find a '../../grf.farm' path relative to the project, and will fail otherwise
copy_docs_to_grf_farm:
	$(_V) $(PYTHON3) src//grf_farm.py polar-fox

clean:
	@ echo "[CLEANING]"
	@ rm -rf src/__pycache__ src/*/__pycache__ bin/__pycache__ generated dist docs
	@ echo "[DONE]"
