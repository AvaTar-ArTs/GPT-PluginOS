.PHONY: test validate compile lock audit site-export release-check

test:
	python -m unittest discover -s tests -v

validate:
	python -m pluginos validate

compile:
	python -m pluginos compile --output pluginos.compiled.json

lock:
	python -m pluginos lock --output pluginos.lock.json

audit:
	python -m pluginos audit

site-export:
	python -m pluginos export-site site/data

release-check: test validate
	python -m pluginos compile --output /tmp/pluginos.compiled.json
	python -m pluginos lock --output /tmp/pluginos.lock.json
	python -m pluginos route media.image.upscale --policy quality-first --json
	python -m pluginos audit
