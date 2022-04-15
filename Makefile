build:
	jb build book

git: build
	git add .
	git status

open:
	google-chrome ./book/_build/html/index.html

update: build git

.PHONY: build git open update