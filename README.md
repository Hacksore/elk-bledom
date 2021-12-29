# elk-bledom

Control Bluetooth LE lights via a WebUI

### Run as docker

Since we need the hosts BLE we put in these flags to allow it to work?

```
docker run --cap-add=SYS_ADMIN --cap-add=NET_ADMIN --net=host -p 8080:8080 hacksore/elk-bledom
```