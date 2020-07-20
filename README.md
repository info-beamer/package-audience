[![Import](https://cdn.infobeamer.com/s/img/import.png)](https://info-beamer.com/use?url=https://github.com/info-beamer/package-audience)

# A face detection example for info-beamer hosted

This package implements a face detector using a connected
Raspberry Pi camera. The package can be run standalone for
debugging purposes or can be added as a child to existing
packages and can trigger events upon detecting a face
within the camera stream.

The detection is done on the device only and works even
completely offline. Detection is reasonably fast.

The code in `service` can be modified if other events should
be triggered upon detection.
