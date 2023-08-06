pip3 install black!=23.1.0

black --check ./ka_com
pipreqs --force --ignore .mypy_cache --mode gt .
mypy ./ka_com

ruff --clean 
ruff --fix ./ka_com

pip3 install .

cd /app/ka_com/ka_com/docs; make man

python3 -m build --wheel --sdist
twine check dist/*
twine upload dist/*
