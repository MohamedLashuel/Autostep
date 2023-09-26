if [ -d bin ]; then
	bin/pip install --force-reinstall ../Autochart/dist/*.whl
else
	pip install --force-reinstall ../Autochart/dist/*.whl
fi