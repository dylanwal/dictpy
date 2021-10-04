This folder contains all the tests. 

To run all checks, in the terminal type:
1. mypy src
2. flake8 src
3. pytest


packaging:
1)py -m build
2)twine upload dist/*

creating Badges
test:
1) pytest --junitxml=reports/junit/junit.xml
2) genbadge tests

coverange

flake8:
1) flake8 src  --exit-zero --format=html --htmldir ./reports/flake8 --statistics --tee --output-file flake8stats.txt
2)

download stats:
`pypistats recent dictpy`
`pypinfo dictpy`    <-- pypi all time download

![Github All Releases](https://img.shields.io/github/downloads/dylanwal/dictpy/total.svg)

