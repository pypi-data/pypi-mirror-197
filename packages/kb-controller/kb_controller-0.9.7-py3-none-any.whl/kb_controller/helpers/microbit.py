from time import sleep
import serial
from . import kb_config

ser = None

def send_message(msg):
    global ser
    if ser is None:
        initialize_connection()

    print('m:b >>> ' + msg)
    ser.write(bytes(msg, 'utf-8'))
    # ensure that the controller do not pick up the message itself 
    sleep(0.2)

def read_line():
    if ser is None:
        initialize_connection()

    text = ser.readline() 
    ser.reset_input_buffer()
    return text

def initialize_connection():
    global ser
    try:
        ser = serial.Serial(kb_config.tty_name, kb_config.tty_rate, timeout=kb_config.tty_timeout)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        print()
        print(f'Forbinder til micro:bit på: {kb_config.tty_name}')
        sleep(0.2)
        send_message('init')
        return ser
    except Exception as e:
        print()
        print(
            f"Der skete en fejl under forbindelse til seriel porten: {kb_config.tty_name}")
        print("Tjek om microbit'en er forbundet, eller om portnavnet er korrekt.")
        print()
        print(type(e))
        print('----')
        print(e.args)
        exit()

def close_connection():
    if not ser is None:
        ser.close()
