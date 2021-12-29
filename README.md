# elk-bledom

Control Bluetooth LE lights via a WebUI

### Running via docker
```
docker run \
  --net=host \
  --restart always \
  --detach \
  --name light \
  hacksore/elk-bledom
```