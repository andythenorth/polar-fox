# Various needed programs
PYTHON3 = python3

FIND_FILES = bin/find-files

.PHONY: dist

dist: $(shell $(FIND_FILES) --ext=.py --ext=.png --ext=.txt src)
	@ $(PYTHON3) bin/build-dist.py

install: dist
	@ $(PYTHON3) bin/install-dist.py

clean:
	$(_V) echo "[CLEANING]"
	@ for f in src/__pycache__ src/*/__pycache__ bin/__pycache__ generated dist; \
	do if test -e $$f;\
	   then rm -r $$f;\
	   fi;\
	done
	@ echo "[DONE]"
