build:
	jb build book

git: build
	git add .
	git status

open:
	google-chrome ./book/_build/html/index.html

update: build git

deploy: build
	ghp-import -n -p -f ./book/_build/html

.PHONY: build git open update deploy