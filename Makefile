build:
	cd client && npm run build
	docker build -t hacksore/elk-bledom .
push:
	docker push hacksore/elk-bledom
test:
	docker run -p 80:80 hacksore/elk-bledom