all: prod


prod:
	sudo chown -R root:root ./PowerManager
	find PowerManager -name "__pycache__" -exec rm -rf {} \;
	find PowerManager -name "*.pyc" -exec rm -rf {} \;
	find PowerManager -type d -exec chmod 0755 {} \;
	find PowerManager -type f -exec chmod 0644 {} \;
	sudo chmod 0755 PowerManager/DEBIAN/postinst
	sudo chmod 0755 PowerManager/DEBIAN/prerm
	sudo chmod +x PowerManager/usr/lib/power-manager/power-manager.py
	sudo chmod +x PowerManager/usr/lib/power-manager/power-manager-indicator.py

	./dpkg-deb-nodot ./PowerManager
	sudo chown -R sensey:sensey ./PowerManager*.deb

dev:
	sudo chown -R sensey:sensey ./PowerManager
