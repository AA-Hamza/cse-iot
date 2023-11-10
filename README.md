# CSE IOT
This project aims to create a basic iot system that can handle different kinds of devices ranging from powerful raspberry pis to small devices like nodemcu (esp8266).

## Design
![image](https://github.com/AA-Hamza/cse-iot/assets/33000142/6f025e29-2286-40df-acd4-4bc411df3bad)
- Every device has it's own device number, you can think of it as the device tenant. No other device has access (read or write) to it, unless explictly shared of course. 
- Every device states it's capabilities stated when it connects to the broker.
  - We mainly support `commands` & `sensors`
  - commands are modules that are connected to the device and can be controlled like lcds, buzzers, motors ....
  - sensors are modules that are connected to the device and can't be controlled like temperature sensors, humidity sensors, light sensors .... 
- Devices can be controlled using the `command` topic with specific data payload to each of the supported commands.
- Devices also return data as feedback in the topic `feedback` when a command is sent

## Our goals
- Having a declartive configuration `config.yaml` that just states connected modules to the device, and the user can use the platform without needing to change code.
- Easily adding more device/module/sensor support.
- Plugin system


## Rock 4c+ testing
- Broker
![image](https://github.com/AA-Hamza/cse-iot/assets/33000142/1f97ce0c-b085-4b78-bf7b-5b0cb1422f3c)
- Results
![Uploading image.png…]()
