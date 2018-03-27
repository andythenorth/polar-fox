# Various needed programs
PYTHON3 = python3

FIND_FILES = bin/find-files

.PHONY: dist

dist: $(shell $(FIND_FILES) --ext=.py --ext=.png --ext=.txt src)
	@ $(PYTHON3) bin/build_dist.py

install: dist
	@ $(PYTHON3) bin/install_dist.py

clean:
	$(_V) echo "[CLEANING]"
	@ rm -rf src/__pycache__ src/*/__pycache__ bin/__pycache__ generated dist
	@ echo "[DONE]"
