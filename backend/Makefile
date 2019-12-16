M = $(shell printf "\033[34;1m▶\033[0m")

build: ; $(info $(M) Building project...)
	go build -mod=vendor -o bin/server main.go

setup: ; $(info $(M) Getting denpendencies...)
	go mod vendor

serve:
	go run main.go

clean:
	rm -rf bin/

.PHONY: build serve clean
