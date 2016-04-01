all: deb


deb: clean
	sudo chown -R sensey:sensey build
	mkdir -p build/usr/bin
	mkdir -p build/usr/lib/power-manager
	cp -r vendor build/usr/lib/power-manager
	cp power-manager.py build/usr/lib/power-manager
	cp power-manager-indicator.py build/usr/lib/power-manager
	ln -rs build/usr/lib/power-manager/power-manager.py build/usr/bin/power-manager
	ln -rs build/usr/lib/power-manager/power-manager-indicator.py build/usr/bin/power-manager-indicator
	#find build -name "__pycache__" -exec rm -rf {} \;
	#find build -name "*.pyc" -exec rm -rf {} \;
	find build -type d -exec chmod 0755 {} \;
	find build -type f -exec chmod 0644 {} \;
	sudo chmod +x build/usr/lib/power-manager/power-manager.py
	sudo chmod +x build/usr/lib/power-manager/power-manager-indicator.py
	./dpkg-deb-nodot build power-manager

clean:
	rm -rf build/usr/bin
	rm -rf build/usr/lib