
test_publish:
	python3 -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade build
	python3 -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org hatchling
	## could not do in isolated env because it was difficult to use the self-signed certificates
	## creates dist/ dir
	python3 -m build -n
	python3 -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade twine
	## added a /etc/pip.conf file with trusted hosts
	#python3 -m twine upload --repository testpypi dist/*
	## twine using this cert: '/home/agsadmin/.local/lib/python3.8/site-packages/certifi/cacert.pem'
	python3 -m twine upload --username __token__ --repository testpypi dist/* --cert  /usr/local/share/ca-certificates/BIT_Proxy_Root_CA_01.crt


test_install:
	python3 -m venv pyfirecrest_helper_testenv
	source pyfirecrest_helper_testenv/bin/activate
	python3 -m pip install --index-url https://test.pypi.org/simple/ --trusted-host pypi.org --trusted-host test.pypi.org --trusted-host test-files.pythonhosted.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --no-deps pyfirecrest-helper
	deactivate
	rm -r pyfirecrest_helper_testenv


publish:
	python3 -m venv pyfirecrest_helper_testenv
	source pyfirecrest_helper_testenv/bin/activate
	python3 -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade build pip setuptools wheel
	python3 -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org hatchling
	## could not do in isolated env because it was difficult to use the self-signed certificates
	## creates dist/ dir
	python3 -m build
	python3 -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade twine
	## added a /etc/pip.conf file with trusted hosts
	## twine using this cert: '/home/agsadmin/.local/lib/python3.8/site-packages/certifi/cacert.pem'
	python3 -m twine upload --username julia.gustavsen dist/* --cert  /usr/local/share/ca-certificates/BIT_Proxy_Root_CA_01.crt
	#rm -fr build dist .egg requests.egg-info


pyinstaller_package:
	python3 -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -U pyinstaller
	pyinstaller pyfirecrest_helper.py
	## need to bundle the files as a zip and then can provide.


test_setup:
	python3 -m venv pyfirecrest_helper_testenv
	source pyfirecrest_helper_testenv/bin/activate
	#python setup.py register sdist upload
	python3 -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade build
	python3 -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade pip setuptools wheel
	python3 -m build
	python3 -m pip install -e pyfirecrest_helper
	deactivate
