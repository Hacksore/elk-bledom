build:
	docker buildx build -t hacksore/elk-bledom --platform linux/arm/v7 .
push:
	docker push hacksore/elk-bledom
test:
	docker run --cap-add=SYS_ADMIN --cap-add=NET_ADMIN --net=host hacksore/elk-bledom