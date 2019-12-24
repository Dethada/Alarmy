image = rpi-opencv

build:
	sudo docker build -t $(image) .

run:
	sudo docker run --rm --name c1-$(image) -it $(image) /bin/bash

clean:
	sudo docker rmi $(image)
