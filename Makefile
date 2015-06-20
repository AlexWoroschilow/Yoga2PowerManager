all: prod


prod:
	sudo chown -R root:root ./PowerManager
	find ./PowerManager -name "__pycache__" -exec rm -rf {} \;
	dpkg-deb --build ./PowerManager
	sudo chown -R sensey:sensey ./PowerManager.deb

dev:
	sudo chown -R sensey:sensey ./PowerManager
