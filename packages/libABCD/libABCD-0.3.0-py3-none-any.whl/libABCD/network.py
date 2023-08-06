import libABCD
import time
import json
import paho.mqtt.client as mqtt


def setserver(ip='localhost',port=9818): # default mosquitto port is 1883!
    libABCD.network_info["host"]=ip
    libABCD.network_info["port"]=port

def ignore(data,topic):
    pass

def statustopic():
    return "@status/"+libABCD.name
def totopic():
    return "@to/"+libABCD.name

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True
        libABCD.logger.info("Connected to server")
        libABCD.publish(statustopic(),'{"on":1,"time":'+str(time.time())+'}',retain=True)
    else:
        client.bad_connection_flag=True

def on_disconnect(client, userdata,rc=0):
    libABCD.logger.error("Disconnected from server, code "+str(rc))
    libABCD.die()

def connect(name="Unknown",cleansession=True):
    libABCD.mqtt=mqtt.Client(name,cleansession)
    libABCD.mqtt.on_connect=on_connect
    libABCD.mqtt.on_disconnect=on_disconnect
    libABCD.mqtt.will_set(statustopic(),'{"on":0,"from":"'+libABCD.name+'"}', qos=0, retain=True)
    libABCD.mqtt.on_message=libABCD.on_message
    libABCD.mqtt.connect(libABCD.network_info["host"],port=libABCD.network_info["port"]) # add port
    libABCD.mqtt.loop_start()
    libABCD.mqtt.subscribe(totopic(),qos=2)
    libABCD.mqtt.subscribe("@broadcast",qos=2)

def disconnect():
    libABCD.publish(statustopic(),'{"on":0,"time":'+str(time.time())+'}',retain=True)
    libABCD.mqtt.disconnect()
    libABCD.mqtt.loop_stop()

def subscribe(topic,qos=2):
    libABCD.mqtt.subscribe(topic,qos)

def publish(topic, payload=None, qos=2, retain=False):
    # check the payload
    try:
        if type(payload) is dict:
            j=payload
        else:
            j=json.loads(payload)
        if not "from" in j:
            j["from"]=libABCD.name
        libABCD.mqtt.publish(topic,json.dumps(j),qos,retain);
    except:
        libABCD.logger.warning('asked to send a message not in JSON format, ignoring {}'.format(payload))

def on_message(client, userdata, message):
    #print("message received " ,str(message.payload.decode("utf-8")))
    #print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)
    #print("message =",message)
    try:
        jsdata=json.loads(message.payload.decode("utf-8"))
    except:
        libABCD.logger.warning('received a payload not in JSON format, ignoring {}'.format(message.payload))
        return
    try:
        if "_default" in libABCD.cmd_switch:
            func=libABCD.cmd_switch["_default"]
        if "cmd" in jsdata:
            if jsdata["cmd"] in libABCD.cmd_switch:
                func=libABCD.cmd_switch[jsdata["cmd"]]
    except Exception as e:
        libABCD.logger.warning('Don\'t know what to do with message {} on topic {}'.format(jsdata,message.topic))
    else:
        try:
            func(jsdata,message.topic)
        except Exception as e:
            libABCD.logger.warning('Function call error {} for message {} on topic {}'.format(e,jsdata,message.topic))


def addmessage(msg):
    libABCD.logger.debug("Using old addmessage function")
    if type(msg) is dict:
        j=msg
    else:
        j=json.loads(msg)
    try:
        libABCD.publish("@to/"+j["to"],json.dumps(j))
    except Exception as e:
        libABCD.logger.warning("Error {}".format(e))
        pass

def hasmessage():
    libABCD.logger.debug("Using old hasmessage function")
    return len(libABCD.network_info["outgoing"])

def close():
    libABCD.logger.debug("Using old close function")
    mysel=libABCD.network_info["selector"]
    connection=libABCD.network_info["socket"]
    mysel.unregister(connection)
    connection.close()
    del libABCD.network_info["socket"]
    libABCD.network_info["isconnected"]=False
    libABCD.network_info["timeconnected"]=0

def handle(timeout=1):
    time.sleep(timeout)
    return


