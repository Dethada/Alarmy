image = postgres-local

build:
	sudo docker build -t $(image) .

run:
	sudo docker run --name c1-$(image) -it $(image) /bin/bash

clean:
	sudo docker rmi $(image)
