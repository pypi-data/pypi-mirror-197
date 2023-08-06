# Autonomous Bariloche Central DAQ

## concept

The main concept for the DAQ is that it orbits around a central server. 
Control and information run through this server allowing a permanent 
follow-up of what is happening. The raw data is handled by the clients 
themselves and is not seen by the DAQ. The central server is a MQTT 
broker. We recommend using mosquitto.

## code

All the code is in the libABCD directory. Documentation for `init`, 
`publish`, `subscribe`, `unsubscribe` and `add_callback` can be found 
as docstrings (more accesible documentation upcoming).
