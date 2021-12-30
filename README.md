# elk-bledom

Control Bluetooth LE lights via a WebUI

![image](https://user-images.githubusercontent.com/996134/147717496-4d759dff-a601-4560-8fb1-c3c0b55bacc0.png)


### Running via docker
```
docker run \
  --net=host \
  --restart always \
  --detach \
  --name light \
  hacksore/elk-bledom
```
