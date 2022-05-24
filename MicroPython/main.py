import machine
from machine import Pin, SoftI2C, PWM
import time
from time import sleep
from LCD_i2c_driver import I2cLcd
from simpleKeyboard import Device
from binascii import hexlify
import json
from buzzer_music import music
from crypto import encode, decode

# LCD setup
I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)     #initializing the I2C method for ESP32
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

# BLE setup
d = Device()

# Keypad setup
KEY_UP   = const(0)
KEY_DOWN = const(1)

buttonDown = 'B'
buttonUp = 'A'

keys = [['1', '2', '3', 'A'], ['4', '5', '6', 'B'], ['7', '8', '9', 'C'], ['*', '0', '#', 'D']]

# Pin names for Pico
rows = [13,12,14,27]
cols = [26,25,33,32]

# set pins for rows as outputs
row_pins = [Pin(pin_name, mode=Pin.OUT) for pin_name in rows]

# set pins for cols as inputs
col_pins = [Pin(pin_name, mode=Pin.IN, pull=Pin.PULL_DOWN) for pin_name in cols]

# Buzzer setup, it turn on the buzzer, on the 2200hz. In order to use mySong, you don't neet to use. It's here only for testing purpose.
#buzzer = PWM(Pin(18), freq=2200, duty=512) #use only to check if the buzzer works

# message of MQTT
last_message = b''

#startup song
song = '8 A5 1 1;6 B5 1 1;4 G5 1 1;2 A5 1 1;1 A5 1 1;0 A5 1 1'
systemBeep = '0 F6 1 43'


def mainLoop():
    data = load_r_credentialsFile()
    fromConnecting = True
    mySong = music(song, pins=[Pin(18)])
    lcd.putstr("Welcome to \nPassChain")
    for i in range(0,30):
        print(mySong.tick())
        sleep(0.04)
        
    sleep(2)
    
    while True:
        if d.isConnected():
            if fromConnecting:
                connectedBle()
                sleep(2)
                fromConnecting = False
                
            lcd.clear()
            select = menuList(data)
            lcd.clear()

            lcd.putstr("Insert pin code:")
            lcd.move_to(0,1)
            pinCode = ''
            direction = ''

            while True:
                direction = read_keypad()

                if direction == 'D':
                    break

                if direction is not None and direction != 'C':
                    pinCode += direction

                lcd.move_to(0,1)
                lcd.putstr(pinCode)

                if direction == 'C':
                    if pinCode == decode(data['pin'], "2005202209"):
                        break
                    else:
                        lcd.clear()
                        lcd.putstr('Wrong pin!')
                        lcd.move_to(0,1)
                        lcd.putstr("Try again.")
                        sleep(2)
                        lcd.clear()
                        lcd.putstr("Insert pin code:")
                        pinCode = ''
                
                time.sleep_ms(160)

            if direction == 'D':
                continue
            
            lcd.clear()
            lcd.putstr("> Username: ****")
            lcd.move_to(0,1)
            lcd.putstr("> Password: ****")
            
            while True:
                if not d.isConnected():
                    break
                
                direction = read_keypad()

                if direction == 'D':
                    break
    
                if direction == buttonDown:
                    lcd.clear()
                    lcd.putstr("Writing")
                    lcd.move_to(0,1)
                    lcd.putstr("password.")
                    time.sleep_ms(250)
                    lcd.putstr(".")
                    time.sleep_ms(250)
                    lcd.putstr(".")
                    d.send_string(decode(data['credentials'][select]['password'], "2005202209"))
                    time.sleep_ms(250)
                    lcd.putstr(".")
                    time.sleep_ms(500)
                    lcd.clear()
                    lcd.putstr("> Username: ****")
                    lcd.move_to(0,1)
                    lcd.putstr("> Password: ****")
                    
                if direction == buttonUp:
                    lcd.clear()
                    lcd.putstr("Writing")
                    lcd.move_to(0,1)
                    lcd.putstr("username.")
                    time.sleep_ms(250)
                    lcd.putstr(".")
                    time.sleep_ms(250)
                    lcd.putstr(".")
                    d.send_string(decode(data['credentials'][select]['username'], "2005202209"))
                    time.sleep_ms(250)
                    lcd.putstr(".")
                    time.sleep_ms(500)
                    lcd.clear()
                    lcd.putstr("> Username: ****")
                    lcd.move_to(0,1)
                    lcd.putstr("> Password: ****")
            
        else:
            d.advertise()
            connectingBle()
            fromConnecting = True
            sleep(2)
            

# BLE functions
def connectingBle():
    lcd.clear()
    lcd.putstr("Connecting.")
    time.sleep_ms(250)
    lcd.putstr(".")
    time.sleep_ms(250)
    lcd.putstr(".")
    time.sleep_ms(250)
    lcd.putstr(".")
    time.sleep_ms(250)
    return

def connectedBle():
    lcd.clear()
    lcd.putstr("The device is\n")
    lcd.putstr("connected !")
    time.sleep_ms(250)
    return


# Keypad functions
def init():
    for row in range(0,4):
        for col in range(0,4):
            row_pins[row].value(0)

def scan(row, col):
    """ scan the keypad """
    # set the current column to high
    row_pins[row].value(1)
    key = None

    # check for keypressed events
    if col_pins[col].value() == KEY_DOWN:
        key = KEY_DOWN
    if col_pins[col].value() == KEY_UP:
        key = KEY_UP
    row_pins[row].value(0)

    # return the key state
    return key

def read_keypad():
    last_key_press = None
    for row in range(4):
        for col in range(4):
            key = scan(row, col)
            if key == KEY_DOWN:
                mySong = music(systemBeep, pins=[Pin(18)])
                for i in range(5):
                    mySong.tick()
                    time.sleep_ms(10)
                    
                last_key_press = keys[row][col]
    return last_key_press


# Json functions
def load_r_credentialsFile():
   with open('credentials.json') as credentials:
       return json.load(credentials)
 
def load_w_credentialsFile(data):
    with open("credentials.json", "w") as credentials:
        json.dump(data, credentials) 
 
def write_credentialsFile(data, name, username, password):
    if name is not None:
        if username is not None:
            if password is not None:
                new_object = {"name": name,
                              "username": username,
                              "password": password
                              }
                data["credentials"].append(new_object)
                load_w_credentialsFile(data)
                return True
    return False
  
def update_credentialsFile(data, name, newName, username, password):
    if name is not None:
        for i in range(0, len(data['credentials'])):
            if data['credentials'][i]['name'] == name:
                
                if newName is not None or not newName:
                    data['credentials'][i]['name'] = newName
                
                if username is not None or not username:
                    data['credentials'][i]['username'] = username
                
                if password is not None or not password:
                    data['credentials'][i]['password'] = password
                    
                load_w_credentialsFile(data)
                return True
    return False

def update_pinCodeFile(data, newPin):
    if newPin is not None:
        data['pin'] = newPin
        load_w_credentialsFile(data)
        return True
    return False
 
def remove_credentialsFile(data, name):
    if name is not None:
        for i in range(0, len(data['credentials'])):
            if data['credentials'][i]['name'] == name:
                del data['credentials'][i]
                
                load_w_credentialsFile(data)
                return True
    return False


# menu credentials list
def menuList(data):
    pos = 0
    lcd.putstr("Authentication")
    lcd.move_to(0,1)
    lcd.putstr('> ' + data['credentials'][pos]['name'])

    while(True): 
        direction = read_keypad()
        
        if(direction == buttonDown) and (pos + 1 < len(data['credentials'])):
            lcd.clear()
            lcd.putstr(data['credentials'][pos]['name'])
            lcd.move_to(0,1)
            pos += 1
            lcd.putstr('> ' + data['credentials'][pos]['name'])
        
        if (direction == buttonUp) and (pos - 1 >= 0):
            lcd.clear()
            pos -= 1
            lcd.putstr('> ' +data['credentials'][pos]['name'])
            lcd.move_to(0,1)
            lcd.putstr(data['credentials'][pos+1]['name'])
            
        if (direction == '*'):
            mqtt_connection(data)
            pos = 0
            lcd.putstr("Authentication")
            lcd.move_to(0,1)
            lcd.putstr('> ' + data['credentials'][pos]['name'])
        
        if read_keypad() == 'C':
            return pos


# MQTT functions
def mqtt_connection(data):
    global last_message, topic_pub
    lcd.clear()
    lcd.putstr("Connecting to")
    lcd.move_to(0,1)
    lcd.putstr("PassChain App")
    try:
      client = connect_and_subscribe()
      client.publish(topic_pub, (json.dumps(data)).encode())
      sleep(1)
    except OSError as e:
      restart_and_reconnect()
    
    lcd.clear()
    lcd.putstr("Connected to")
    lcd.move_to(0,1)
    lcd.putstr("PassChain App!")
    
    while True:
        if last_message == b'reconnect':
            client.publish(topic_pub, (json.dumps(data)).encode())
            last_message = b''
                        
        direction = read_keypad()
        try:
            client.check_msg()
            if last_message != b'' and last_message != b'reconnect':
                msg = last_message.decode("utf-8")
                
                if msg[0:2] == "00":
                    credential = msg[2:].split(",")
                    write_credentialsFile(data, credential[0], credential[1], credential[2])
                    client.publish(topic_pub, (json.dumps(data)).encode())
                    
                elif msg[0:2] == "01":
                    credential = msg[2:].split(",")
                    update_credentialsFile(data, credential[0], credential[1], credential[2], credential[3])
                    client.publish(topic_pub, (json.dumps(data)).encode())
                    
                elif msg[0:2] == "02":
                    remove_credentialsFile(data, msg[2:])
                    client.publish(topic_pub, (json.dumps(data)).encode())
                    
                elif msg[0:2] == "03":
                    update_pinCodeFile(data, msg[2:])
                    client.publish(topic_pub, (json.dumps(data)).encode())
                    
                last_message = b''
                
        except OSError as e:
            restart_and_reconnect()
            
        if direction == 'D':
            client.publish(topic_pub, "disconnect")
            client.disconnect()
            return

def sub_cb(topic, msg):
    global last_message
    last_message = msg
    if topic == b'notification' and msg == b'received':
        print('ESP received hello message')

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()      
        

if __name__ == "__main__":
    mainLoop()