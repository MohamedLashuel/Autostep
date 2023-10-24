if [ ! -d ../Autochart ]; then
	git clone https://github.com/MohamedLashuel/Autochart ..
fi
cd ../Autochart
python -m build
cd ../Autostep
source .venv/bin/activate
pip uninstall -y autochart
pip install ../Autochart/dist/*.whl