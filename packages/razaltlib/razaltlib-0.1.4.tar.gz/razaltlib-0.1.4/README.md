Startd following https://johnfraney.ca/blog/create-publish-python-package-poetry/

to publish to pypi:
poetry build
poetry publish

poetry cache clear pypi --all && poetry update razaltlib


