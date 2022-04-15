build:
	jb build data-science-escalavel

copy: build
	cp -r data-science-escalavel/_build/html/* docs

git: copy
	git add .
	git status

open:
	google-chrome ./data-science-escalavel/_build/html/index.html

update: build copy git

.PHONY: build copy git open update