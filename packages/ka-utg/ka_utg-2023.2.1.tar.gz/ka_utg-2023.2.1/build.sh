pip3 install black!=23.1.0

black --check ./ka_utg
pipreqs --force --ignore .mypy_cache --mode gt .
mypy ./ka_utg

ruff --clean 
ruff --fix ./ka_utg

pip3 install .

cd /app/ka_utg/ka_utg/docs; make man

python3 -m build --wheel --sdist
twine check dist/*
twine upload dist/*
