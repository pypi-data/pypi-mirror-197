from time import sleep
from serial import Serial
from serial.tools.list_ports import comports
from serial import tools
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
        print(f'Forbinder til micro:bit på: {kb_config.tty_name}')
        ser = Serial(kb_config.tty_name, kb_config.tty_rate, timeout=kb_config.tty_timeout)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        sleep(0.2)
        send_message('init')
        return ser
    except Exception as e:
        print()
        print('-------------------------------------')
        print("FEJL under etablering af forbindelse!")
        print(e.args)
        print()
        print("Tjek om microbit'en er forbundet, eller om portnavnet er korrekt.")
        ports = comports()
        if len(ports) > 0:
            print()
            print('Tilgængelige porte:')
            for port in ports:
                print(port)
        print('-------------------------------------')
        print()
        exit()

def close_connection():
    if not ser is None:
        ser.close()
