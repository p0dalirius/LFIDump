.PHONY: all access firstrun build start stop

IMAGE := poc_lfi_dump

all : stop build firstrun

build:
	@docker build -t ${IMAGE}:latest -f Dockerfile .

firstrun:
	@docker run -it -p 8000:80 ${IMAGE}

access:
	docker exec -it $(shell docker ps | grep ${IMAGE} | awk '{split($$0,a," "); print a[1]}') /bin/bash

start:
	@if [ $(shell docker ps -a | grep ${IMAGE} | head -n1 | awk '{split($$0,a," "); print a[1]}' | wc -l) -eq 0 ]; then \
		echo "[+] Building image ${IMAGE} ..." ;\
		make build ;\
	fi
	@if [ $(shell docker ps -f status=running | grep ${IMAGE} | head -n1 | wc -l) -ne 0 ]; then \
		echo "[+] Instance $(shell docker ps -a | grep ${IMAGE} | head -n1 | awk '{split($$0,a," "); print a[1]}') of image ${IMAGE} is already running." ;\
	else \
                echo "[+] Starting instance $(shell docker ps -a | grep ${IMAGE} | head -n1 | awk '{split($$0,a," "); print a[1]}') of image ${IMAGE} ..." ;\
		docker start $(shell docker ps -a | grep ${IMAGE} | head -n1 | awk '{split($$0,a," "); print a[1]}') ;\
                echo "[+] Done !"; \
	fi

stop:
	@if [ $(shell docker ps -f status=running | grep ${IMAGE} | head -n1 | wc -l) -eq 0 ]; then \
		echo "[+] Instance $(shell docker ps -a | grep ${IMAGE} | head -n1 | awk '{split($$0,a," "); print a[1]}') of image ${IMAGE} was found but is not running." ;\
	else \
                echo "[+] Stopping instance $(shell docker ps -a | grep ${IMAGE} | head -n1 | awk '{split($$0,a," "); print a[1]}') of image ${IMAGE} ..." ;\
		docker stop $(shell docker ps -a | grep ${IMAGE} | head -n1 | awk '{split($$0,a," "); print a[1]}') -t 1 ;\
                echo "[+] Done !"; \
	fi
