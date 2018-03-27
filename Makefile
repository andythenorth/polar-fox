# Various needed programs
PYTHON3 = python3

FIND_FILES = bin/find-files

.PHONY: dist

dist: $(shell $(FIND_FILES) --ext=.py --ext=.png --ext=.txt src)
	$(_V) $(PYTHON3) bin/distribute.py