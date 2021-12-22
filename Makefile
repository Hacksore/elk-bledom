build:
	docker build -t hacksore/elk-bledom .
test:
	docker run --cap-add=SYS_ADMIN --cap-add=NET_ADMIN --net=host -p 8080:8080 hacksore/elk-bledom