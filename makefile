py=python

server: server.py docker/server.dockerfile
	$(py) server.py

client: client.py docker/client.dockerfile
	$(py) client.py

testing: ./test/
	pytest ./test/