run:
	env INKWELL_CONFIG_MODULE=inkwell.config.LocalConfig python app.py

install:
	python setup.py develop

uninstall:
	python setup.py develop --uninstall

clean:
	find . -name \*.pyc -exec rm {\} \; ; rm -rf build/ dist/ *.egg-info *.egg