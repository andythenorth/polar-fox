# Various needed programs
PYTHON3 = python3

FIND_FILES = bin/find-files

.PHONY: dist cargo_graphics clean install

dist: cargo_graphics $(shell $(FIND_FILES) --ext=.py --ext=.txt src)
	@ $(PYTHON3) src/build_dist.py

cargo_graphics: $(shell $(FIND_FILES) --ext=.py --ext=.png src)
	@ $(PYTHON3) src/render_cargo_graphics.py

install: dist
	@ $(PYTHON3) src/install_dist.py

clean:
	@ echo "[CLEANING]"
	@ rm -rf src/__pycache__ src/*/__pycache__ bin/__pycache__ generated dist
	@ echo "[DONE]"
