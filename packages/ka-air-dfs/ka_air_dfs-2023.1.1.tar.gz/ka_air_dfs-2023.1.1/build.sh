pip3 install black!=23.1.0

black --check ./ka_air_dfs
pipreqs --force --ignore .mypy_cache .
mypy ./ka_air_dfs
ruff --fix ./ka_air_dfs
pip3 install .

cd /app/ka_air_dfs/ka_air_dfs/docs; make man
cd /app/ka_air_dfs/ka_air_dfs/docs; make man

python3 -m build --wheel --sdist
twine check dist/*
twine upload dist/*
