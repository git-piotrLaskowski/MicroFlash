# Micro Python Touch Robot
## 1. Erasing board:

Remember to change port (COM5) to actual one on your PC

```shell
$ esptool.py --port COM12 erase_flash
```

## 2. Flashing board:


```shell
$ esptool.py --port COM12 write_flash -z 0x1000 ESP32_GENERIC-20241025-v1.24.0.bin
```

## 2. Flash firmware

To flash firmware just run 
```shell
$ python flash_ESP.py
```
via python configuration. WIth micropython plugin 
it may not work. Remember to check COM port.
    