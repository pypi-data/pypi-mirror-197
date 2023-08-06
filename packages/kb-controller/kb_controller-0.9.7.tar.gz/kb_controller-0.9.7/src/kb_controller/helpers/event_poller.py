from threading import Thread
from time import sleep
from datetime import datetime
from . import microbit
from . import kb_config
from . import kb_central

stop_thread = False
thread = None

def kb_central_poller(current_track_id):
    sleep(1) # Give controller time to initialize
    global stop_thread
    while True:
        print()
        print('- - - - - - - - - - - - - - - - - - - - -')
        print(f"{datetime.now()} POLLER CENTRAL...")

        count = kb_central.get_number_of_events_for_track(current_track_id)
        microbit.send_message(f'EVENT-TRACKS:{current_track_id}:{count}')

        print(f'Kontakter kuglebane-centralen igen om {kb_config.poll_interval_in_seconds} sekunder...')
        print('- - - - - - - - - - - - - - - - - - - - -')
        print()
        sleep(kb_config.poll_interval_in_seconds)
        if (stop_thread):
            print('QUIT signal modtaget - stopper med at polle kuglebane controlleren!')
            break

def start_thread(current_track_id):
    print()
    print(f'Starter tråd der poller kb-centralen: {kb_config.kbc_host}')
    global thread
    if thread is None and not stop_thread:
        thread = Thread(group=None, target=kb_central_poller, args=(current_track_id,))
        thread.start()

def signal_stop_thread():
    global stop_thread
    stop_thread = True