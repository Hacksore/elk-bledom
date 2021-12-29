build:
	docker build -t hacksore/elk-bledom .
push:
	docker push hacksore/elk-bledom
test:
	docker run -p 8080:8080 hacksore/elk-bledom