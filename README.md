This repository will contain the code that will measure the level of beer remaining in the kegs

# Notes
I had to uninstall the GPIO package and install lgpio since GPIO is not natively supported for RPI5

```pip3 uninstall rpi-lgpio```

```sudo apt install python3-rpi.gpio```

Sensor 1 is connected on GPIO5 an GPIO6
Sensor 2 is connected on GPIO9 and GPIO10
