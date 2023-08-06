pip3 install black!=23.1.0

black --check ./ka_uts
pipreqs --force --ignore .mypy_cache --mode gt .
mypy ./ka_uts

ruff --clean
ruff --fix ./ka_uts

pip3 install .

cd /app/ka_uts/ka_uts/docs; make man

python3 -m build --wheel --sdist
twine check dist/*
twine upload dist/*
